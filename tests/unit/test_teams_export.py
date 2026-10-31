"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from office365.graph_client import GraphClient
from office365.migration import MigrationJob
from office365.migration.teams import TeamsArchiveSource, TeamsArchiveTarget, TeamsExportOptions
from tests._scripted_transport import RecordingTransport, ScriptedTransport

_TEAM = {"id": "t1", "displayName": "Alpha", "visibility": "public", "mailNickname": "alpha"}
_CHANNELS = {"value": [{"id": "c1", "displayName": "General", "membershipType": "standard"}]}
_MESSAGES = {"value": [{"id": "msg1", "body": {"content": "hi"}, "createdDateTime": "2024-01-01T10:00:00Z"}]}
_REPLIES = {"value": []}


def _client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def _options() -> TeamsExportOptions:
    return TeamsExportOptions(include_members=False, include_tabs=False, include_apps=False)


def test_archive_job_round_trip(tmp_path: Path):
    payloads = [
        _CHANNELS,  # source.list_items -> channels
        _MESSAGES,  # source.list_items -> messages
        _REPLIES,  # replies
        _TEAM,  # run: structure read
        _TEAM,  # verify: structure checksum
    ]
    client = _client(ScriptedTransport(payloads))
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
    assert team["displayName"] == "Alpha"
    lines = (tmp_path / "t1" / "messages.ndjson").read_text().strip().splitlines()
    assert json.loads(lines[0])["channel_id"] == "c1"


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
    transport = RecordingTransport([{"value": []}])
    client = _client(transport)

    client.chats.get_all_messages().filter("createdDateTime gt 2024-01-01T00:00:00Z").execute_query()

    assert any("getAllMessages" in url for url in transport.urls)
    assert any("$filter" in url for url in transport.urls)


def test_visible_history_start_datetime_is_set():
    client = _client(ScriptedTransport([]))
    team = client.teams["t1"]
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)

    member = team.members.add(user="u1", roles=["member"], visible_history_start_datetime=start)

    assert member.get_property("visibleHistoryStartDateTime") == start


def test_download_hosted_contents_deferred(tmp_path):
    client = _client(ScriptedTransport([{"value": [_MESSAGE]}, b"\x89PNG"]))
    channel = client.teams["t1"].channels["c1"]

    channel.messages.get_all().download_hosted_contents(tmp_path).execute_query()

    assert (tmp_path / "m1_hc1.png").read_bytes() == b"\x89PNG"


def test_archive_keeps_what_the_model_spells_and_not_a_copy_of_it(tmp_path: Path):
    message = {**_MESSAGE, "id": "msg1"}
    payloads = [
        _CHANNELS,  # plan: channels
        {"value": [message]},  # plan: messages
        _REPLIES,  # plan: replies
        _TEAM,  # run: the team
        {"value": [{"id": "m1", "displayName": "Alice", "roles": ["owner"], "email": "a@x.com"}]},
        {"value": [{"id": "app1", "teamsAppDefinition": {"teamsAppId": "ta1", "displayName": "Planner"}}]},
        {"value": [{"id": "cm1", "displayName": "Bob", "roles": []}]},  # the channel's members
        {"value": [{"id": "tab1", "displayName": "Wiki", "teamsApp": {"id": "wiki"}}]},
    ]
    client = _client(ScriptedTransport(payloads))
    options = TeamsExportOptions(include_hosted_contents=False)
    job = MigrationJob(TeamsArchiveSource(client, ["t1"], options), TeamsArchiveTarget(tmp_path))
    job.plan()
    job.run()

    team = json.loads((tmp_path / "t1" / "team.json").read_text())
    assert team["displayName"] == "Alpha"
    assert team["members"][0]["roles"] == ["owner"]
    assert team["installedApps"][0]["teamsAppDefinition"]["teamsAppId"] == "ta1"
    channel = team["channels"][0]
    assert channel["displayName"] == "General"
    assert channel["members"][0]["displayName"] == "Bob"
    assert channel["tabs"][0]["teamsApp"]["id"] == "wiki"

    line = json.loads((tmp_path / "t1" / "messages.ndjson").read_text().splitlines()[0])
    assert line["channel_id"] == "c1"
    assert line["from"]["user"]["displayName"] == "Alice"  # JSON, not the repr of a typed object
    assert line["mentions"][0]["mentionText"] == "@Bob"
