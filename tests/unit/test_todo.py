"""Offline tests for Microsoft To Do attachments, properties, and extensions."""

from __future__ import annotations

import base64

from office365.graph_client import GraphClient
from office365.todo.attachments.collection import AttachmentBaseCollection
from office365.todo.attachments.task_file import TaskFileAttachment
from office365.todo.tasks.lists.list import TodoTaskList
from office365.todo.tasks.wellknownlistname import WellknownListName
from tests._scripted_transport import ScriptedTransport


class _CaptureTransport(ScriptedTransport):
    def __init__(self, payloads):
        super().__init__(payloads)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        return super().execute(request)


def _client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def _task(client):
    return client.me.todo.lists["l1"].tasks["t1"]


def test_attachments_collection_type_and_small_add():
    client = _client(ScriptedTransport([]))
    task = _task(client)

    assert isinstance(task.attachments, AttachmentBaseCollection)
    attachment = task.attachments.add("hello.txt", b"hello", "text/plain")

    assert isinstance(attachment, TaskFileAttachment)
    assert attachment.get_property("name") == "hello.txt"
    assert attachment.get_property("contentBytes") == base64.b64encode(b"hello").decode("ascii")
    assert attachment.get_property("size") == 5  # noqa: PLR2004


def test_create_upload_session_parses_url():
    client = _client(
        ScriptedTransport(
            [
                {
                    "uploadUrl": "https://upload.example/session",
                    "expirationDateTime": "2024-01-01T00:00:00Z",
                    "nextExpectedRanges": ["0-"],
                }
            ]
        )
    )
    task = _task(client)

    session = task.attachments.create_upload_session(
        "big.bin", 5 * 1024 * 1024, "application/octet-stream"
    ).execute_query()

    assert session.upload_url == "https://upload.example/session"
    assert list(session.next_expected_ranges) == ["0-"]


def test_upload_attachment_small_uses_simple_post():
    transport = _CaptureTransport([{"id": "a1", "name": "small.txt"}])
    client = _client(transport)
    task = _task(client)

    attachment = task.upload_attachment(b"small", name="small.txt", content_type="text/plain")

    assert isinstance(attachment, TaskFileAttachment)
    posted = [r for r in transport.requests if isinstance(r.data, dict)]
    assert any(r.data.get("@odata.type") == "#microsoft.graph.taskFileAttachment" for r in posted)


def test_upload_attachment_large_uses_session_and_chunks():
    transport = _CaptureTransport(
        [
            {"uploadUrl": "https://upload.example/session", "nextExpectedRanges": ["0-"]},
            {"id": "a1"},
            {"id": "a1"},
        ]
    )
    client = _client(transport)
    task = _task(client)

    task.upload_attachment(b"x" * (5 * 1024 * 1024), name="big.bin", chunk_size=4 * 1024 * 1024)

    puts = [r for r in transport.requests if getattr(r.method, "value", r.method) == "PUT"]
    assert len(puts) == 2  # noqa: PLR2004
    assert puts[0].headers["Content-Range"].startswith("bytes 0-")


def test_list_properties_and_extension():
    client = _client(ScriptedTransport([]))
    task_list = TodoTaskList(client)
    task_list.set_property("isOwner", True)
    task_list.set_property("isShared", False)
    task_list.set_property("wellknownListName", "defaultList")

    assert task_list.is_owner is True
    assert task_list.is_shared is False
    assert task_list.wellknown_list_name == WellknownListName.defaultList

    extension = task_list.add_extension("com.example.ext", custom="value")
    assert extension.get_property("extensionName") == "com.example.ext"
    assert extension.get_property("custom") == "value"
