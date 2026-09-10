"""Offline tests for Teams message export primitives (Phase 0)."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from office365.graph_client import GraphClient
from office365.runtime.transport.base import BaseTransport
from office365.teams.chats.messages.hosted_content import ChatMessageHostedContent
from requests import Response
from tests._scripted_transport import ScriptedTransport

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


def _client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


class _CaptureTransport(BaseTransport):
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
    client = _client(ScriptedTransport([{"value": [_MESSAGE]}]))
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
    transport = _CaptureTransport(content=json.dumps({"value": []}).encode(), content_type="application/json")
    client = _client(transport)

    client.chats.get_all_messages().filter("createdDateTime gt 2024-01-01T00:00:00Z").execute_query()

    assert any("getAllMessages" in url for url in transport.urls)
    assert any("$filter" in url for url in transport.urls)


def test_hosted_content_get_content():
    transport = _CaptureTransport(content=b"\x89PNG", content_type="application/octet-stream")
    client = _client(transport)
    hosted = ChatMessageHostedContent(client)

    result = hosted.get_content().execute_query()

    assert result.value == b"\x89PNG"
    assert any("$value" in url for url in transport.urls)


def test_visible_history_start_datetime_is_set():
    client = _client(ScriptedTransport([]))
    team = client.teams["t1"]
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)

    member = team.members.add(user="u1", roles=["member"], visible_history_start_datetime=start)

    assert member.get_property("visibleHistoryStartDateTime") == start


def test_download_hosted_contents_deferred(tmp_path):
    client = _client(
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
