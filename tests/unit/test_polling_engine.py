"""The polling engine: one wait, three things layered on it.

:class:`~office365.runtime.operation.Operation` is the base -- what a subclass supplies,
what it inherits, and the two things a family configures as data (``transient_statuses``
and ``jitter``). :class:`~office365.runtime.pollable.PollableOperation` adds waitable
operation *entities* (plus the async twin ``TeamsAsyncOperation`` uses), and
:mod:`office365.runtime.lro` reads Graph/Azure operation-status documents: classifying
them, resolving the poll URL (``Operation-Location`` / ``Azure-AsyncOperation`` /
``Location`` / ``original-url``), pacing by ``Retry-After``, continuation tokens, cancel,
and the awaitable twin.

The three were separate files with three clocks and two copies of the same status-document
helper. They are one mechanism, so they are one file, sharing one clock and one helper.
"""

import asyncio
import threading
import time
from datetime import datetime, timezone
from typing import Any

import pytest
from office365.graph_client import GraphClient
from office365.migration.offline import offline_sharepoint_context
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.lro import ContinuationToken, OperationPoller, resolve_poll_url
from office365.runtime.operation import (
    Operation,
    OperationCancelledError,
    OperationFailedError,
    OperationStatus,
    OperationTimeoutError,
)
from office365.runtime.pollable import (
    PollableOperation,
    is_transient_poll_error,
    next_poll_delay,
)
from office365.sharepoint.client_context import ClientContext
from office365.teams.operations.async_operation import wait_for_operation_async
from office365.teams.operations.async_status import TeamsAsyncOperationStatus
from tests._scripted_transport import (
    AsyncScriptedTransport,
    RoutingTransport,
    ScriptedTransport,
    build_response,
)


class _Clock:
    """Injectable monotonic clock whose ``sleep`` advances time."""

    def __init__(self) -> None:
        self.t = 0.0
        self.slept: list[float] = []

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds

    async def asleep(self, seconds: float) -> None:
        self.sleep(seconds)


class _Scripted(Operation[Any]):
    """An operation whose attempts are a script of (status, http_status) pairs."""

    def __init__(self, script: list[tuple[str | None, int]], **options: Any) -> None:
        super().__init__(**options)
        self._script = list(script)
        self.attempts = 0

    def _step(self) -> OperationStatus:
        self.attempts += 1
        status, http_status = self._script.pop(0)
        return OperationStatus(status=status, http_status=http_status)

    async def _step_async(self) -> OperationStatus:
        return self._step()


def _run(script: list[tuple[str | None, int]], **options: Any) -> _Scripted:
    clock = options.pop("clock", None) or _Clock()
    options.setdefault("clock", clock.now)
    options.setdefault("sleep", clock.sleep)
    options.setdefault("async_sleep", clock.asleep)
    operation = _Scripted(script, **options)
    operation.clock = clock  # type: ignore[attr-defined]
    return operation


def test_stream_yields_every_snapshot_terminal_last():
    operation = _run([("inProgress", 202), ("inProgress", 202), ("completed", 200)])
    statuses = list(operation.stream())
    assert [s.status for s in statuses] == ["inProgress", "inProgress", "completed"]
    assert operation.attempts == 3  # noqa: PLR2004
    assert operation.last_status is statuses[-1]


def test_wait_returns_the_terminal_snapshot():
    status = _run([("inProgress", 202), ("completed", 200)]).wait()
    assert status.status == "completed"
    assert status.is_success


def test_progress_callback_sees_every_snapshot():
    seen: list[str] = []
    operation = _run([("inProgress", 202), ("completed", 200)], on_progress=lambda s: seen.append(s.status or ""))
    operation.wait()
    assert seen == ["inProgress", "completed"]


def test_a_family_can_declare_its_transient_status_is_not_an_observation():
    """Reported by default; a *gap* is a family''s decision, taken by override."""

    class _GapIsSilent(_Scripted):
        def _observable(self, status: OperationStatus) -> bool:
            return status.http_status not in {404}

    clock = _Clock()
    operation = _GapIsSilent(
        [(None, 404), ("inProgress", 202), ("completed", 200)],
        transient_statuses=frozenset({404, 429, 503}),
        clock=clock.now,
        sleep=clock.sleep,
    )
    assert [s.status for s in operation.stream()] == ["inProgress", "completed"]


def test_a_transient_status_outside_the_set_is_terminal():
    """The default set is the monitor-URL one: a ``404`` there is the answer."""
    operation = _run([(None, 404)])
    status = operation.wait(raise_on_failure=False)
    assert status.http_status == 404  # noqa: PLR2004
    assert operation.attempts == 1


def test_jitter_zero_is_exact_and_jitter_spreads():
    exact = _run([("inProgress", 202), ("completed", 200)], interval=10.0)
    exact.wait()
    assert exact.clock.slept == [10.0]  # type: ignore[attr-defined]

    for _ in range(20):
        spread = _run([("inProgress", 202), ("completed", 200)], interval=10.0, jitter=0.2)
        spread.wait()
        delay = spread.clock.slept[0]  # type: ignore[attr-defined]
        assert 8.0 <= delay <= 12.0  # noqa: PLR2004


def test_retry_after_wins_over_the_interval():
    class _RetryAfter(_Scripted):
        def _step(self) -> OperationStatus:
            status = super()._step()
            status.retry_after = 30.0
            return status

    clock = _Clock()
    operation = _RetryAfter([("inProgress", 202), ("completed", 200)], clock=clock.now, sleep=clock.sleep)
    operation.wait()
    assert clock.slept == [30.0]


def test_timeout_raises_the_shared_error_family():
    """One timeout error for every wait: it is also a ``TimeoutError``."""
    operation = _run([("inProgress", 202)] * 100, interval=10.0, timeout=25.0)
    with pytest.raises(OperationTimeoutError) as caught:
        operation.wait()
    assert caught.value.timeout == 25.0  # noqa: PLR2004
    assert isinstance(caught.value, TimeoutError)
    # Never sleeps past the deadline: the third poll would land at 30s > 25s.
    assert operation.clock.slept == [10.0, 10.0]  # type: ignore[attr-defined]


def test_cancel_wakes_a_blocking_wait_from_another_thread():
    """The pause is an event, so a 30 s ``interval`` does not delay a cancel.

    No injected ``sleep``: the default pause is the interruptible one.
    """
    polled = threading.Event()
    raised: list[BaseException] = []

    class _Blocked(Operation[Any]):
        def _step(self) -> OperationStatus:
            polled.set()
            return OperationStatus(status="inProgress", http_status=202)

    operation = _Blocked(interval=30.0)

    def wait() -> None:
        try:
            operation.wait()
        except BaseException as error:  # noqa: BLE001 - asserted below
            raised.append(error)

    thread = threading.Thread(target=wait)
    thread.start()
    assert polled.wait(timeout=5)
    started = time.monotonic()
    operation.cancel()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert time.monotonic() - started < 1.0  # noqa: PLR2004 - a 30 s pause, not a 30 s wait
    assert isinstance(raised[0], OperationCancelledError)


def test_astream_is_the_same_script():
    operation = _run([("inProgress", 202), ("completed", 200)])

    async def collect() -> list[str]:
        return [s.status async for s in operation.astream() if s.status]

    assert asyncio.run(collect()) == ["inProgress", "completed"]


def test_wait_async_raises_the_same_family():
    operation = _run([("failed", 200)])
    with pytest.raises(OperationFailedError):
        asyncio.run(operation.wait_async())


def test_cancelled_task_stops_waiting_only_by_default():
    sent: list[str] = []

    class _SendsCancel(_Scripted):
        def _send_cancel(self) -> None:
            sent.append("sync")

        async def _send_cancel_async(self) -> None:
            sent.append("async")

    async def run(**options: Any) -> None:
        operation = _SendsCancel([("inProgress", 202)] * 5, interval=30.0)
        task = asyncio.ensure_future(operation.wait_async(**options))
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(run())
    assert sent == []
    asyncio.run(run(cancel_on_task_cancel=True))
    assert sent == ["async"]


_URL = "https://graph.microsoft.com/v1.0/sites/root/operations/1"


def _lro(http_status: int, body: Any = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"http_status": http_status}
    if body is not None:
        payload["body"] = body
    if headers is not None:
        payload["headers"] = headers
    return payload


def _operation_response(http_status: int, body: Any = None, headers: dict[str, str] | None = None) -> Any:
    return build_response(RequestOptions(url=_URL), _lro(http_status, body, headers))


def _not_found() -> ClientRequestException:
    return ClientRequestException.from_response(_operation_response(404, {"error": {"code": "NotFound"}}))


class _FakeOperation(PollableOperation):
    """Minimal host exposing just ``properties`` (the mixin's only runtime need)."""

    def __init__(self, properties: dict[str, Any] | None = None) -> None:
        self.properties = properties or {}


def test_is_transient_poll_error():
    assert is_transient_poll_error(_not_found())
    assert is_transient_poll_error(ClientRequestException.from_response(_operation_response(503)))
    assert not is_transient_poll_error(ClientRequestException.from_response(_operation_response(500)))


def test_next_poll_delay_honors_retry_after():
    assert next_poll_delay(_operation_response(202, headers={"Retry-After": "7"}), 10) == 7.0  # noqa: PLR2004
    assert next_poll_delay(_operation_response(202), 10) == 10.0  # noqa: PLR2004
    assert next_poll_delay(None, 3) == 3.0  # noqa: PLR2004


def test_pollable_wait_async_completes(monkeypatch: pytest.MonkeyPatch):
    clock = _Clock()
    responses = iter(
        [
            _operation_response(202, {"status": "running"}, {"Retry-After": "1"}),
            _operation_response(202, {"status": "succeeded"}),
        ]
    )

    async def _reload(_op: Any) -> Any:
        return next(responses)

    monkeypatch.setattr("office365.runtime.pollable.reload_operation_async", _reload)
    op = _FakeOperation({"status": "running"})
    result = asyncio.run(op.wait_async(clock=clock.now, async_sleep=clock.asleep))
    assert result is op
    assert clock.t == 1.0


def test_pollable_completion_helpers():
    assert _FakeOperation({"status": "completed"}).is_operation_complete
    assert not _FakeOperation({"status": "completed"}).is_operation_failed
    assert _FakeOperation({"status": "failed"}).is_operation_failed
    assert not _FakeOperation({"status": "running"}).is_operation_complete


def test_rich_long_running_operation_wait():
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = ScriptedTransport(
        [
            _lro(200, {"status": "running"}),
            _lro(200, {"status": "completed", "resourceId": "res", "resourceLocation": "https://loc"}),
        ]
    )
    operation = client.sites["root"].operations["op1"]
    operation.wait(interval=0)
    assert operation.properties["status"] == "completed"
    assert operation.resource_id == "res"
    assert operation.resource_location == "https://loc"


def test_pollable_stream_raises_nothing_for_a_failed_outcome(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "office365.runtime.pollable.reload_operation",
        lambda op: _operation_response(202, {"status": "failed", "error": {"code": "x"}}),
    )
    op = _FakeOperation({"status": "failed"})
    statuses = list(op.stream(clock=_Clock().now, sleep=_Clock().sleep))
    assert len(statuses) == 1
    assert statuses[0].is_failure
    with pytest.raises(OperationFailedError):
        op.wait(clock=_Clock().now, sleep=_Clock().sleep)


def test_teams_poll_for_status_blocks_until_succeeded():
    """The sync twin polls to completion itself instead of queueing a callback chain."""
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = ScriptedTransport(
        [
            _lro(404, {"error": {"code": "NotFound", "message": "not created yet"}}),
            _lro(200, {"status": "inProgress"}),
            _lro(200, {"status": "succeeded", "targetResourceId": "t1"}),
        ]
    )
    operation = client.teams["teamid"].operations["opid"]
    seen: list[str] = []

    result = operation.poll_for_status(
        polling_interval=0, timeout_sec=30, success_callback=lambda _op: seen.append("success")
    )

    assert result is operation
    assert seen == ["success"]
    assert operation.target_resource_id == "t1"
    assert client.pending_request().transport.calls == 3  # noqa: PLR2004 - 404 gap, then two polls


def _teams_client(payloads: list[Any]) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request()._async_transport = AsyncScriptedTransport(payloads)
    return client


def test_teams_poll_for_status_async_succeeds_with_404_gap():
    client = _teams_client(
        [
            _lro(404, {"error": {"code": "NotFound", "message": "not created yet"}}),
            _lro(200, {"status": "succeeded", "targetResourceId": "t1"}),
        ]
    )
    operation = client.teams["teamid"].operations["opid"]
    seen: list[str] = []
    result = asyncio.run(
        operation.poll_for_status_async(
            TeamsAsyncOperationStatus.succeeded,
            timeout_sec=30,
            polling_interval=0,
            success_callback=lambda _op: seen.append("success"),
            failure_callback=lambda _op: seen.append("failure"),
        )
    )
    assert result is operation
    assert seen == ["success"]
    assert operation.operation_status == "succeeded"


def test_teams_poll_for_status_async_reports_failure():
    client = _teams_client([_lro(200, {"status": "failed", "error": {"code": "bad"}})])
    operation = client.teams["teamid"].operations["opid"]
    seen: list[str] = []
    asyncio.run(
        operation.poll_for_status_async(
            TeamsAsyncOperationStatus.succeeded,
            timeout_sec=30,
            polling_interval=0,
            failure_callback=lambda _op: seen.append("failure"),
        )
    )
    assert seen == ["failure"]


def test_teams_poll_for_status_async_times_out():
    client = _teams_client([_lro(200, {"status": "running"})])
    operation = client.teams["teamid"].operations["opid"]
    seen: list[str] = []
    asyncio.run(
        operation.poll_for_status_async(
            TeamsAsyncOperationStatus.succeeded,
            timeout_sec=0,
            polling_interval=0,
            failure_callback=lambda _op: seen.append("timeout"),
        )
    )
    assert seen == ["timeout"]


def test_wait_for_operation_async_raises_on_failure():
    client = _teams_client([_lro(200, {"status": "failed"})])
    operation = client.teams["teamid"].operations["opid"]
    with pytest.raises(RuntimeError, match="Async operation failed"):
        asyncio.run(wait_for_operation_async(operation, timeout_sec=30, interval=0))


_MONITOR = "https://api.onedrive.com/monitor/abc"


def _ctx() -> ClientContext:
    ctx = offline_sharepoint_context()
    ctx.pending_request().beforeExecute.clear()
    return ctx


def _response(http_status: int, body: Any = None, headers: dict[str, str] | None = None) -> Any:
    request = RequestOptions(url=_MONITOR)
    return build_response(request, _lro(http_status, body, headers))


def _poller(transport: Any, clock: _Clock, **kwargs: Any) -> OperationPoller:
    options: dict[str, Any] = {"clock": clock.now, "sleep": clock.sleep, "async_sleep": clock.asleep}
    options.update(kwargs)
    return OperationPoller(_ctx(), _MONITOR, transport=transport, **options)


def test_status_parses_graph_progress():
    status = OperationStatus.from_response(
        _response(202, {"status": "inProgress", "percentageComplete": 27.8, "resourceLocation": "https://r"})
    )
    assert status.status == "inProgress"
    assert status.http_status == 202  # noqa: PLR2004
    assert status.percentage_complete == 27.8  # noqa: PLR2004
    assert status.resource_location == "https://r"
    assert not status.is_terminal
    assert not status.is_success
    assert not status.is_failure


def test_status_200_without_body_is_terminal_success():
    status = OperationStatus.from_response(_response(200))
    assert status.status is None
    assert status.is_success
    assert status.is_terminal


def test_wait_stops_on_partially_succeeded():
    # The regression: an unknown status is "keep polling", so a partially
    # succeeded job was polled until `OperationTimeoutError`.
    clock = _Clock()
    transport = ScriptedTransport([_lro(200, {"status": "PartiallySucceeded"})])
    status = _poller(transport, clock, interval=3).wait()
    assert status.is_partially_succeeded
    assert transport.calls == 1


def test_status_reads_timestamps_and_retry_after():
    status = OperationStatus.from_response(
        _response(
            202,
            {
                "status": "inProgress",
                "createdDateTime": "2026-10-21T09:00:00Z",
                "lastActionDateTime": "2026-10-21T09:05:30.0000000+02:00",
            },
            {"Retry-After": "7"},
        )
    )
    # Timestamps are timezone-aware, so an age is an honest subtraction.
    assert status.created_date_time == datetime(2026, 10, 21, 9, 0, tzinfo=timezone.utc)
    assert status.last_action_date_time == datetime(2026, 10, 21, 7, 5, 30, tzinfo=timezone.utc)
    assert status.retry_after == 7.0  # noqa: PLR2004

    # A value the parser cannot read is absent, never a guess.
    unreadable = OperationStatus.from_response(_response(202, {"status": "inProgress", "createdDateTime": "soon"}))
    assert unreadable.created_date_time is None
    assert unreadable.retry_after is None


def test_resolve_poll_url_final_state_via():
    resp = _response(202, {"status": "running"}, {"Location": "https://l", "Azure-AsyncOperation": "https://a"})
    assert resolve_poll_url(resp, final_state_via="location") == "https://l"
    assert resolve_poll_url(resp, final_state_via="azure-async-operation") == "https://a"
    assert resolve_poll_url(resp, final_state_via="original-url", original_url="https://orig") == "https://orig"


def test_from_response_requires_monitor_url():
    with pytest.raises(ValueError, match="monitor URL"):
        OperationPoller.from_response(_ctx(), _response(200))


def test_from_response_builds_poller():
    resp = _response(202, {"status": "running"}, {"Location": _MONITOR})
    poller = OperationPoller.from_response(_ctx(), resp)
    assert poller.poll_url == _MONITOR
    assert poller.final_state_via == "auto"
    assert poller.last_status is None


def test_wait_raises_client_exception_on_permanent_error():
    from office365.runtime.client_request_exception import ClientRequestException

    transport = ScriptedTransport([_lro(404, {"error": {"code": "gone"}})])
    with pytest.raises(ClientRequestException):
        _poller(transport, _Clock()).wait()


def test_stream_returns_a_failed_terminal_status_instead_of_raising():
    transport = ScriptedTransport([_lro(202, {"status": "failed", "error": {"code": "x"}})])
    seen = list(_poller(transport, _Clock()).stream())
    assert [s.status for s in seen] == ["failed"]
    assert seen[-1].is_failure


def test_astream_yields_every_snapshot():
    clock = _Clock()
    transport = AsyncScriptedTransport(
        [
            _lro(202, {"status": "inProgress"}, {"Retry-After": "1"}),
            _lro(202, {"status": "completed", "resourceId": "9"}),
        ]
    )
    poller = OperationPoller(_ctx(), _MONITOR, async_transport=transport, clock=clock.now, async_sleep=clock.asleep)

    async def collect() -> list[OperationStatus]:
        return [status async for status in poller.astream()]

    seen = asyncio.run(collect())
    assert [s.status for s in seen] == ["inProgress", "completed"]
    assert seen[-1].resource_id == "9"
    assert clock.t == 1.0


def test_continuation_token_round_trip():
    transport = ScriptedTransport([_lro(202, {"status": "completed"})])
    poller = _poller(transport, _Clock(), final_state_via="location")
    poller.wait()
    token = poller.to_continuation_token()
    assert token.status == "completed"

    restored = OperationPoller.from_continuation_token(_ctx(), token.to_json())
    assert restored.poll_url == _MONITOR
    assert restored.final_state_via == "location"

    from_mapping = ContinuationToken.from_json({"poll_url": _MONITOR})
    assert from_mapping.status is None
    assert from_mapping.final_state_via == "auto"


def test_wait_raises_cancelled_error():
    transport = ScriptedTransport([_lro(202, {"status": "cancelled"})])
    with pytest.raises(OperationCancelledError) as excinfo:
        _poller(transport, _Clock()).wait()
    assert excinfo.value.status.is_cancelled
    # OperationCancelledError is an OperationFailedError, so old handlers still catch it.
    assert isinstance(excinfo.value, OperationFailedError)


def test_cancel_sends_service_request():
    clock = _Clock()
    cancel_url = "https://api.onedrive.com/operations/abc"
    transport = RoutingTransport(
        [
            (_MONITOR, _lro(202, {"status": "inProgress"})),
            (cancel_url, {"http_status": 204}),
        ]
    )
    cancel_request = RequestOptions(url=cancel_url, method=HttpMethod.Post)
    poller = OperationPoller(
        _ctx(),
        _MONITOR,
        transport=transport,
        cancel_request=cancel_request,
        clock=clock.now,
        sleep=clock.sleep,
    )
    poller.cancel()
    assert transport.calls == [cancel_url]


def test_wait_async_stops_when_cancelled():
    clock = _Clock()
    transport = AsyncScriptedTransport([_lro(202, {"status": "completed"})])
    poller = OperationPoller(_ctx(), _MONITOR, async_transport=transport, clock=clock.now, async_sleep=clock.asleep)
    poller.cancel()
    with pytest.raises(OperationCancelledError):
        asyncio.run(poller.wait_async())
    assert transport.calls == 0


def test_wait_async_forwards_cancel_on_task_cancel():
    clock = _Clock()
    transport = AsyncScriptedTransport([_lro(202, {"status": "inProgress"}), {"http_status": 204}])
    cancel_request = RequestOptions(url="https://api.onedrive.com/operations/abc", method=HttpMethod.Post)

    async def asleep(_seconds: float) -> None:
        raise asyncio.CancelledError

    poller = OperationPoller(
        _ctx(),
        _MONITOR,
        async_transport=transport,
        cancel_request=cancel_request,
        clock=clock.now,
        async_sleep=asleep,
    )
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(poller.wait_async(cancel_on_task_cancel=True))
    assert transport.calls == 2  # noqa: PLR2004 - one poll + one cancel request


def test_cancel_async_wakes_wait_async_promptly():
    clock = _Clock()
    transport = AsyncScriptedTransport([_lro(202, {"status": "inProgress"}, {"Retry-After": "2"})])
    poller = OperationPoller(_ctx(), _MONITOR, async_transport=transport, clock=clock.now, interval=2)

    async def scenario() -> None:
        task = asyncio.ensure_future(poller.wait_async())
        await asyncio.sleep(0.05)
        await poller.cancel_async()
        with pytest.raises(OperationCancelledError):
            await asyncio.wait_for(task, timeout=1)

    asyncio.run(scenario())
    assert transport.calls == 1


def test_cancel_from_thread_wakes_wait_async():
    clock = _Clock()
    transport = AsyncScriptedTransport([_lro(202, {"status": "inProgress"}, {"Retry-After": "2"})])
    poller = OperationPoller(_ctx(), _MONITOR, async_transport=transport, clock=clock.now, interval=2)

    async def scenario() -> None:
        timer = threading.Timer(0.05, poller.cancel)
        timer.start()
        try:
            with pytest.raises(OperationCancelledError):
                await asyncio.wait_for(poller.wait_async(), timeout=1)
        finally:
            timer.cancel()

    asyncio.run(scenario())
    assert transport.calls == 1
