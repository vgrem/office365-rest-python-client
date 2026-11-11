"""What a service layers on top of the generic poller: a result, and a submission verb.

:class:`~office365.runtime.lro.LongRunningOperationResult` is what a Graph long-running
action hands back for a monitor URL, and
:class:`~office365.onedrive.driveitems.copy_result.DriveItemCopyResult` turns a completed
``driveItem.copy`` into the freshly created item.

:class:`~office365.runtime.respond_async.RespondAsyncRequest` is the other end: it bridges
the OData ``respond-async`` preference (as used by Excel workbook operations) onto the same
poller -- a ``202 Accepted`` becomes a waitable operation, a synchronous answer becomes one
that is already terminal, and that answer also lands in the query's regular result.
"""

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest
from office365.graph_client import GraphClient
from office365.onedrive.driveitems.copy_result import DriveItemCopyResult
from office365.onedrive.listitems.item_reference import ItemReference
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_result import ClientResult
from office365.runtime.lro import LongRunningOperationResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.respond_async import RespondAsyncRequest
from tests._scripted_transport import AsyncScriptedTransport, ScriptedTransport, build_response, graph

_MONITOR = "https://graph.microsoft.com/monitor/abc"


def _lro(http_status: int, body: Any = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"http_status": http_status}
    if body is not None:
        payload["body"] = body
    if headers is not None:
        payload["headers"] = headers
    return payload


def _graph_client(
    *,
    sync_payloads: list[Any] | None = None,
    async_payloads: list[Any] | None = None,
) -> GraphClient:
    client = graph(sync_payloads)[0]
    if async_payloads is not None:
        client.pending_request()._async_transport = AsyncScriptedTransport(list(async_payloads))
    return client


def test_long_running_result_wait_async():
    client = _graph_client(
        async_payloads=[
            _lro(202, {"status": "inProgress"}, {"Retry-After": "0"}),
            _lro(202, {"status": "completed", "resourceId": "9"}),
        ]
    )
    result = LongRunningOperationResult(client, _MONITOR)
    status = asyncio.run(result.wait_async())
    assert status.is_success
    assert result.resource_id == "9"


def test_long_running_result_streams_snapshots():
    client = _graph_client(
        sync_payloads=[
            _lro(202, {"status": "inProgress", "percentageComplete": 12}, {"Retry-After": "0"}),
            _lro(202, {"status": "completed", "resourceId": "42"}),
        ]
    )
    result = LongRunningOperationResult(client, _MONITOR)
    seen = [status.status for status in result.stream()]
    assert seen == ["inProgress", "completed"]
    # A stream keeps the result's view current, so `cancel()` and the resource
    # properties work the same as after `wait()`.
    assert result.last_status is not None
    assert result.last_status.is_success
    assert result.resource_id == "42"


def test_long_running_result_astream():
    client = _graph_client(
        async_payloads=[
            _lro(202, {"status": "inProgress"}, {"Retry-After": "0"}),
            _lro(202, {"status": "completed", "resourceId": "9"}),
        ]
    )
    result = LongRunningOperationResult(client, _MONITOR)

    async def collect() -> list[str | None]:
        return [status.status async for status in result.astream()]

    assert asyncio.run(collect()) == ["inProgress", "completed"]
    assert result.resource_id == "9"


def test_completed_result_is_terminal_without_a_monitor():
    response = build_response(SimpleNamespace(url=_MONITOR), {"http_status": 200, "body": {"id": "1"}})
    result = LongRunningOperationResult.completed(_graph_client(), response)
    assert result.is_completed
    assert result.monitor_url is None
    assert result.last_status is not None
    assert result.last_status.status == "completed"
    # No poll is attempted, so a result without a monitor URL is still waitable.
    assert result.wait() is result.last_status
    assert [s.status for s in result.stream()] == ["completed"]
    assert asyncio.run(result.wait_async()) is result.last_status
    with pytest.raises(ValueError, match="monitor URL"):
        result.to_poller()


def test_copy_result_resolves_item_from_resource_location():
    client = _graph_client(
        sync_payloads=[
            _lro(
                202,
                {
                    "status": "completed",
                    "resourceId": "01ITEM",
                    "resourceLocation": "https://graph.microsoft.com/v1.0/drives/drive1/items/01ITEM",
                },
            ),
            {"id": "01ITEM", "name": "report (copy).xlsx"},
        ]
    )
    result = DriveItemCopyResult(client, None)
    result.set_property("__value", _MONITOR)
    item = result.wait_for_item()
    assert item.id == "01ITEM"
    assert item.name == "report (copy).xlsx"


def test_copy_result_falls_back_to_body_item():
    client = _graph_client(sync_payloads=[_lro(200, {"id": "01ITEM", "name": "copy.xlsx"})])
    result = DriveItemCopyResult(client, None)
    result.set_property("__value", _MONITOR)
    item = result.wait_for_item()
    assert item.id == "01ITEM"
    assert item.name == "copy.xlsx"


def test_drive_item_copy_returns_waitable_result():
    client = _graph_client(sync_payloads=[_lro(202, headers={"Location": "https://graph.microsoft.com/monitor/xyz"})])
    source = client.drives["d1"].items["src"]
    result = source.copy(name="copy.xlsx", parent=ItemReference(driveId="d1", id="dest"))
    assert isinstance(result, DriveItemCopyResult)
    result.execute_query()
    assert result.monitor_url == "https://graph.microsoft.com/monitor/xyz"
    assert result.destination_drive_id == "d1"


_OPERATION_URL = "https://graph.microsoft.com/v1.0/drives/d1/items/i1/workbook/operations/op1"


def _report_query(client: GraphClient) -> tuple[ClientResult[bytes], FunctionQuery]:
    result: ClientResult[bytes] = ClientResult(client, bytes())
    query = FunctionQuery(
        client.reports, "getEmailActivityUserDetail", {"period": "D7"}, result, return_raw_content=True
    )
    return result, query


def test_sync_completion_populates_query_result():
    client = _graph_client(sync_payloads=[_lro(200, b"User,Count\nalice,3\n")])
    result, query = _report_query(client)
    operation = RespondAsyncRequest(client, query).execute()
    assert result.value == b"User,Count\nalice,3\n"
    # The preference was refused: the operation is born terminal, so a caller that
    # opted into the async pattern does not branch on which way the service answered.
    assert operation.is_completed
    assert operation.monitor_url is None
    assert operation.last_status is not None
    assert operation.last_status.http_status == 200  # noqa: PLR2004
    assert operation.last_status.is_success


def test_sync_completion_waits_without_a_request():
    transport = ScriptedTransport([_lro(200, b"csv")])
    client = _graph_client()
    client.pending_request().transport = transport
    _, query = _report_query(client)
    operation = RespondAsyncRequest(client, query).execute()
    status = operation.wait()
    assert status.is_success
    assert [s.status for s in operation.stream()] == ["completed"]
    assert transport.calls == 1  # only the submission; nothing was polled


def test_accepted_returns_pollable_result_and_waits():
    client = _graph_client(
        sync_payloads=[
            _lro(202, headers={"Location": _OPERATION_URL}),
            _lro(202, {"status": "inProgress"}, {"Retry-After": "0"}),
            _lro(200, {"status": "completed", "resourceId": "42"}),
        ]
    )
    result, query = _report_query(client)
    operation = RespondAsyncRequest(client, query).execute()
    assert isinstance(operation, LongRunningOperationResult)
    assert operation.monitor_url == _OPERATION_URL
    status = operation.wait(interval=0.0)
    assert status.is_success
    assert operation.resource_id == "42"
    # The synchronous result must stay untouched on the async path.
    assert result.value == b""


def test_error_status_raises():
    client = _graph_client(sync_payloads=[_lro(403, {"error": {"code": "Forbidden"}})])
    _, query = _report_query(client)
    with pytest.raises(ClientRequestException):
        RespondAsyncRequest(client, query).execute()


def test_async_accepted_can_be_polled():
    client = _graph_client(
        async_payloads=[
            _lro(202, headers={"Location": _OPERATION_URL}),
            _lro(200, {"status": "completed", "resourceId": "7"}),
        ]
    )
    _, query = _report_query(client)
    operation = asyncio.run(RespondAsyncRequest(client, query).execute_async())
    assert not operation.is_completed  # accepted: terminal only after polling
    status = asyncio.run(operation.wait_async(interval=0.0))
    assert status.is_success
    assert operation.resource_id == "7"
