"""Running work that is not one request: the wait, its async twin, and the fan-out.

Everything expensive in this library is one of two shapes -- a long-running operation whose
progress only a poll can tell you, and a fan-out across a thread pool. Both were written three
times each (monitor URL, operation entity, service job counter) and disagreed about what a
deadline is, what a terminal-but-not-failed status is, and what a cancel means; and the
``_async`` twin of every loop was written by copying the loop.

So the claims here are about the engine, not about a service: a deadline that counts the time a
poll itself took, a ``partiallySucceeded`` that ends the wait without raising, a cancel that
never asks the service for a rollback, an async twin that reaches the same verdict through the
same code, and a fan-out that returns results in the order the tasks were given.

No transport takes part. A step here is a Python callable, so a service's own status names are
the only thing borrowed -- the expensive path is asserted without a request, which is the point:
a rule about a deadline is not a fact about a tenant.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from office365.runtime.operation import (
    Operation,
    OperationCancelledError,
    OperationFailedError,
    OperationStatus,
    OperationTimeoutError,
)
from office365.runtime.parallel import run_parallel
from office365.sharepoint.client_context import ClientContext

#: A service that answers "the work is running" this many times before it finishes.
POLLS_BEFORE_DONE = 3

#: How many workers a fan-out is given when the test cares about the pool, not the size.
WORKERS = 3

#: The interval a test pretends a poll takes, and the pace it asks between them.
ONE_SECOND = 1.0

#: What a status has to say to be terminal by its HTTP code alone.
NO_CONTENT = 204


class Scripted(Operation[str]):
    """An operation whose every poll is ``script``: one status per attempt, then the last."""

    def __init__(self, script: list[OperationStatus], *, cost: float = 0.0, **options: Any) -> None:
        super().__init__(**options)
        self._script = list(script)
        self._cost = cost
        self.polls = 0
        self.time = 0.0
        self.cancelled = False

    def _step(self) -> OperationStatus:
        return self._take()

    async def _step_async(self) -> OperationStatus:
        return self._take()

    def _send_cancel(self) -> None:
        self.cancelled = True

    async def _send_cancel_async(self) -> None:
        self.cancelled = True

    def _take(self) -> OperationStatus:
        status = self._script[min(self.polls, len(self._script) - 1)]
        self.polls += 1
        self.time += self._cost  # a poll that takes as long as the network would
        return status


def busy(http_status: int = 202) -> OperationStatus:
    """A poll the service answered "still working"."""
    return OperationStatus(status="inProgress", http_status=http_status)


def done() -> OperationStatus:
    return OperationStatus(status="completed", http_status=200)


def clock_of(operation: Scripted):
    def clock() -> float:
        return operation.time

    return clock


# --- one wait, four claims -----------------------------------------------------------


def test_the_wait_stops_on_the_first_terminal_status_and_reports_progress() -> None:
    seen: list[str | None] = []
    operation = Scripted([busy(), busy(), done()], interval=0.0, sleep=lambda _: None)

    result = operation.wait(on_progress=lambda status: seen.append(status.status))

    assert result.is_success
    assert operation.polls == POLLS_BEFORE_DONE
    # A hook sees every attempt, and the wait hands back the same snapshot it stopped on.
    assert seen == ["inProgress", "inProgress", "completed"]
    assert operation.last_status is result


def test_a_deadline_counts_the_poll_it_just_paid_for() -> None:
    """The defect this pins: a loop that adds its interval and ignores the request's duration.

    One poll costs a second, the budget is two, and every attempt is still busy -- so the second
    poll may not be sent at all. A wait that only counted sleeps would poll past its timeout
    forever against a slow endpoint.
    """
    operation = Scripted([busy()], interval=0.5, cost=ONE_SECOND, timeout=2 * ONE_SECOND)
    operation._clock = clock_of(operation)  # noqa: SLF001 - the clock is the subject here
    operation._sleep = lambda _: None  # noqa: SLF001 - the sleeps are not what is measured

    with pytest.raises(OperationTimeoutError):
        operation.wait()

    # Two polls of a second each are the whole budget. A loop that only counted its sleeps would
    # believe a quarter of a second had passed and send two more.
    assert operation.polls == 2  # noqa: PLR2004 - the number of polls is the claim


def test_a_wait_that_could_not_fit_the_next_poll_does_not_sleep_first() -> None:
    delays: list[float] = []
    operation = Scripted([busy(), done()], interval=2.0, sleep=delays.append)

    operation.wait(timeout=10)

    assert delays == [2.0], "a paused wait spends what the service asked for, and only that"


def test_the_services_own_retry_after_beats_the_interval() -> None:
    delays: list[float] = []
    operation = Scripted([OperationStatus(status="inProgress", http_status=202, retry_after=7.0), done()], interval=1.0)
    operation._sleep = delays.append  # noqa: SLF001 - the pause is the subject

    operation.wait()

    assert delays == [7.0]


# --- a terminal status is not the same question as a failed one ----------------------


def test_a_partial_success_ends_the_wait_without_raising() -> None:
    """``partiallySucceeded`` says the work stopped and item-level failures were reported.

    Polling again would not change it, so the wait must return; raising would make a caller
    that lost one file out of a thousand lose the report that says which one.
    """
    operation = Scripted([OperationStatus(status="partiallySucceeded", http_status=200)])

    status = operation.wait()

    assert status.is_partially_succeeded
    assert not status.is_failure, "a partial success is not a failure of the operation"
    assert operation.polls == 1


def test_a_failure_raises_unless_the_caller_asked_for_the_snapshot() -> None:
    failed = OperationStatus(status="failed", http_status=200, error={"code": "Denied"})

    with pytest.raises(OperationFailedError):
        Scripted([failed]).wait()
    assert Scripted([failed]).wait(raise_on_failure=False).error == {"code": "Denied"}


def test_a_cancelled_status_raises_its_own_error_and_is_still_a_failure() -> None:
    cancelled = OperationStatus(status="cancelled", http_status=200)

    with pytest.raises(OperationCancelledError):
        Scripted([cancelled]).wait()
    # Backward compatibility: a handler written for a failure keeps working.
    assert isinstance(OperationCancelledError(cancelled), OperationFailedError)
    assert cancelled.is_cancelled and cancelled.is_failure


def test_a_stream_yields_the_failure_and_raises_nothing() -> None:
    failed = OperationStatus(status="failed", http_status=200)

    assert [s.status for s in Scripted([busy(), failed], interval=0.0).stream()] == ["inProgress", "failed"]


def test_a_cancel_before_the_wait_reports_cancelled_without_polling() -> None:
    operation = Scripted([busy(), done()])
    operation.cancel()

    status = operation.wait(raise_on_failure=False)

    assert status.is_cancelled
    assert operation.polls == 0, "the caller's own cancellation is not a reason to ask the service"
    assert operation.cancelled, "the service is still asked to stop"


def test_a_transient_status_is_not_an_outcome_even_when_it_looks_terminal() -> None:
    """A ``429`` on a monitor URL is a poll that must be retried, not a finished operation."""
    throttled = OperationStatus(status="inProgress", http_status=429)
    operation = Scripted([throttled, done()], interval=0.0, transient_statuses=frozenset({429, 503}))

    assert operation.wait().is_success
    assert operation.polls == 2  # noqa: PLR2004 - one retried poll, then the answer


# --- the same loop, awaited ----------------------------------------------------------


def test_the_async_wait_reaches_the_same_verdict_through_the_same_rules() -> None:
    script = [busy(), busy(), done()]

    async def run() -> tuple[OperationStatus, str]:
        operation = Scripted(script, interval=0.0, async_sleep=_no_pause)
        return await operation.wait_async(), str(operation.polls)

    status, polls = asyncio.run(run())

    assert status.is_success
    assert polls == str(POLLS_BEFORE_DONE)


def test_an_awaited_stream_yields_what_the_blocking_one_does() -> None:
    script = [busy(), OperationStatus(status="partiallySucceeded", http_status=200)]

    async def run() -> list[str | None]:
        operation = Scripted(script, interval=0.0, async_sleep=_no_pause)
        return [status.status async for status in operation.astream()]

    assert asyncio.run(run()) == ["inProgress", "partiallySucceeded"]


async def _no_pause(_: float) -> None:
    """The async twin of ``sleep=lambda _: None``: a wait that costs no wall time."""


# --- the fan-out ---------------------------------------------------------------------


def test_a_fan_out_returns_results_in_the_order_the_tasks_were_given() -> None:
    results = run_parallel(lambda _ctx, task: task * 2, [3, 1, 2], concurrency=3)

    assert results == [6, 2, 4], "a thread pool finishes out of order; the answer may not"


def test_a_failing_task_is_the_callers_fallback_and_the_rest_still_run() -> None:
    def worker(_ctx, task: int) -> int:
        if task < 0:
            raise ValueError(task)
        return task

    assert run_parallel(worker, [1, -1, 2], on_error=lambda task, _ex: f"failed {task}") == [1, "failed -1", 2]


def test_a_failing_task_with_no_handler_raises_from_the_pool() -> None:
    def worker(_ctx, task: int) -> int:
        raise ValueError(task)

    with pytest.raises(ValueError):
        run_parallel(worker, [1])


def test_each_worker_gets_its_own_context_and_progress_is_reported_once_per_task() -> None:
    made: list[ClientContext] = []
    reported: list[int] = []

    def factory() -> ClientContext:
        made.append(ClientContext("https://contoso.sharepoint.com"))
        return made[-1]

    def worker(ctx: ClientContext, task: int) -> ClientContext:
        return ctx

    contexts = run_parallel(
        worker, [1, 2, 3], concurrency=WORKERS, context_factory=factory, progress=lambda p: reported.append(p.done)
    )

    # One context per worker thread, never one per task: the fleet is what the limiter paces.
    assert len(made) <= WORKERS
    assert len({id(ctx) for ctx in contexts}) == len(made)
    assert all(ctx.rate_limiter is not None for ctx in made), "the pool's contexts share one fleet pacing"
    assert sorted(reported) == [1, 2, 3], "progress counts each completed task once, in any order"
