"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from office365.graph_client import GraphClient
from office365.migration import MigrationJob
from office365.migration.base import MigrationItem
from office365.migration.teams import TeamsArchiveSource, TeamsArchiveTarget, TeamsExportOptions
from office365.runtime.transport.base import BaseTransport
from office365.teams.chats.messages.hosted_content import ChatMessageHostedContent
from requests import Response
from tests._scripted_transport import ScriptedTransport

_TEAM = {"id": "t1", "displayName": "Alpha", "visibility": "public", "mailNickname": "alpha"}
_CHANNELS = {"value": [{"id": "c1", "displayName": "General", "membershipType": "standard"}]}
_MESSAGES = {"value": [{"id": "msg1", "body": {"content": "hi"}, "createdDateTime": "2024-01-01T10:00:00Z"}]}
_REPLIES = {"value": []}


class _Transport(BaseTransport):
    def __init__(self, payloads: list[tuple[str, object]]):
        super().__init__()
        self._payloads = payloads

    def execute(self, request):
        kind, payload = self._payloads.pop(0)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        if kind == "raw":
            resp.headers["Content-Type"] = "application/octet-stream"
            resp._content = payload  # type: ignore[assignment]
        else:
            resp.headers["Content-Type"] = "application/json"
            resp._content = json.dumps(payload).encode()
        return resp


def teamsarchive__client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def _options() -> TeamsExportOptions:
    return TeamsExportOptions(include_members=False, include_tabs=False, include_apps=False)


def test_archive_job_round_trip(tmp_path: Path):
    payloads = [
        ("json", _CHANNELS),  # source.list_items -> channels
        ("json", _MESSAGES),  # source.list_items -> messages
        ("json", _REPLIES),  # replies
        ("json", _TEAM),  # run: structure read
        ("json", _TEAM),  # verify: structure checksum
    ]
    client = teamsarchive__client(_Transport(payloads))
    job = MigrationJob(
        TeamsArchiveSource(client, ["t1"], _options()),
        TeamsArchiveTarget(tmp_path),
    )

    job.plan()
    stats = job.run()
    report = job.verify()

    assert stats.success == 2  # noqa: PLR2004
    assert report.ok
    team = json.loads((tmp_path / "t1" / "team.json").read_text())
    assert team["display_name"] == "Alpha"
    lines = (tmp_path / "t1" / "messages.ndjson").read_text().strip().splitlines()
    assert json.loads(lines[0])["channel_id"] == "c1"


def test_target_round_trip(tmp_path: Path):
    target = TeamsArchiveTarget(tmp_path)
    structure = MigrationItem(source_path="t1/team.json", dest_path="t1/team.json", item_type="structure")
    messages = MigrationItem(source_path="t1/messages.ndjson", dest_path="t1/messages.ndjson", item_type="messages")
    attachment = MigrationItem(
        source_path="t1/attachments/c1/msg1_hc1.png", dest_path="t1/attachments/c1/msg1_hc1.png", item_type="attachment"
    )

    target.write(structure, {"id": "t1"})
    target.write(messages, [{"id": "msg1"}])
    target.write(attachment, b"\x89PNG")

    assert set(target.list_paths()) == {
        "t1/team.json",
        "t1/messages.ndjson",
        "t1/attachments/c1/msg1_hc1.png",
    }
    assert target.exists(structure)
    assert target.checksum(attachment) == target.checksum(attachment)


_MESSAGE = {
    "id": "m1",
    "replyToId": "root1",
    "messageType": "message",
    "etag": "e1",
    "createdDateTime": "2024-01-01T10:00:00Z",
    "lastModifiedDateTime": "2024-01-01T10:05:00Z",
    "from": {"user": {"id": "u1", "displayName": "Alice"}},
    "body": {"contentType": "html", "content": "hello"},
    "mentions": [{"id": 0, "mentionText": "@Bob"}],
    "reactions": [{"reactionType": "like"}],
    "hostedContents": [{"id": "hc1", "contentType": "image/png"}],
}


def teamsmessages__client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


class teamsmessages__CaptureTransport(BaseTransport):
    def __init__(self, content: bytes = b"", content_type: str = "application/octet-stream"):
        super().__init__()
        self.urls: list[str] = []
        self._content = content
        self._content_type = content_type

    def execute(self, request):
        self.urls.append(request.url)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp.headers["Content-Type"] = self._content_type
        resp._content = self._content
        return resp


class _QueueTransport(BaseTransport):
    def __init__(self, payloads: list[tuple[str, object]]):
        super().__init__()
        self._payloads = payloads

    def execute(self, request):
        kind, payload = self._payloads.pop(0)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        if kind == "raw":
            resp.headers["Content-Type"] = "application/octet-stream"
            resp._content = payload  # type: ignore[assignment]
        else:
            resp.headers["Content-Type"] = "application/json"
            resp._content = json.dumps(payload).encode()
        return resp


def test_team_get_all_messages_parses_rich_fields():
    client = teamsmessages__client(ScriptedTransport([{"value": [_MESSAGE]}]))
    messages = client.teams.get_all_messages().execute_query()

    assert len(messages) == 1
    message = messages[0]
    assert message.id == "m1"
    assert message.reply_to_id == "root1"
    assert message.message_type == "message"
    assert message.etag == "e1"
    assert message.from_.user.displayName == "Alice"
    assert len(message.mentions) == 1
    assert len(message.reactions) == 1
    assert message.hosted_contents[0].id == "hc1"


def test_chat_get_all_messages_filter_in_url():
    transport = teamsmessages__CaptureTransport(
        content=json.dumps({"value": []}).encode(), content_type="application/json"
    )
    client = teamsmessages__client(transport)

    client.chats.get_all_messages().filter("createdDateTime gt 2024-01-01T00:00:00Z").execute_query()

    assert any("getAllMessages" in url for url in transport.urls)
    assert any("$filter" in url for url in transport.urls)


def test_hosted_content_get_content():
    transport = teamsmessages__CaptureTransport(content=b"\x89PNG", content_type="application/octet-stream")
    client = teamsmessages__client(transport)
    hosted = ChatMessageHostedContent(client)

    result = hosted.get_content().execute_query()

    assert result.value == b"\x89PNG"
    assert any("$value" in url for url in transport.urls)


def test_visible_history_start_datetime_is_set():
    client = teamsmessages__client(ScriptedTransport([]))
    team = client.teams["t1"]
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)

    member = team.members.add(user="u1", roles=["member"], visible_history_start_datetime=start)

    assert member.get_property("visibleHistoryStartDateTime") == start


def test_download_hosted_contents_deferred(tmp_path):
    client = teamsmessages__client(
        _QueueTransport(
            [
                ("json", {"value": [_MESSAGE]}),
                ("raw", b"\x89PNG"),
            ]
        )
    )
    channel = client.teams["t1"].channels["c1"]

    channel.messages.get_all().download_hosted_contents(tmp_path).execute_query()

    assert (tmp_path / "m1_hc1.png").read_bytes() == b"\x89PNG"


def _item(item_id: str, name: str) -> dict:
    return {"id": item_id, "name": name, "folder": {}, "@odata.type": "#microsoft.graph.driveItem"}


def _not_found() -> dict:
    return {"error": {"code": "itemNotFound", "message": "Item not found"}}


class driveitemensurefolder__CaptureTransport(BaseTransport):
    def __init__(self, responses: list[tuple[int, dict]]):
        super().__init__()
        self._responses = responses
        self.urls: list[str] = []

    def execute(self, request):
        status, body = self._responses.pop(0)
        self.urls.append(request.url)
        resp = Response()
        resp.status_code = status
        resp.url = request.url
        resp.headers["Content-Type"] = "application/json"
        resp._content = json.dumps(body).encode()
        return resp


class TestDriveItemEnsureFolder(unittest.TestCase):
    def _client(self) -> tuple[GraphClient, driveitemensurefolder__CaptureTransport]:
        client = GraphClient()
        transport = driveitemensurefolder__CaptureTransport(
            [
                (404, _not_found()),  # GET a
                (201, _item("a1", "a")),  # POST a
                (200, _item("a1", "a")),  # GET a (reload)
                (404, _not_found()),  # GET a/b
                (201, _item("b2", "b")),  # POST b
                (200, _item("b2", "b")),  # GET a/b (reload)
                (404, _not_found()),  # GET a/b/c
                (201, _item("c3", "c")),  # POST c
                (200, _item("c3", "c")),  # GET a/b/c (reload)
            ]
        )
        client.pending_request().beforeExecute.clear()
        client.pending_request().transport = transport
        return client, transport

    def test_creates_missing_nested_folders(self):
        client, transport = self._client()

        target = client.me.drive.root.ensure_folder("a/b/c")
        client.execute_query()

        posts = [url for url in transport.urls if "children" in url]
        self.assertEqual(len(posts), 3)  # noqa: PLR2004
        self.assertEqual(target.get_property("id"), "c3")
        self.assertEqual(target.get_property("name"), "c")
