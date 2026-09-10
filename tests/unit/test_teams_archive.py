"""Offline tests for the Teams archive adapters (MigrationJob unified API)."""

from __future__ import annotations

import json
from pathlib import Path

from office365.graph_client import GraphClient
from office365.migration import MigrationJob
from office365.migration.base import MigrationItem
from office365.migration.teams import (
    TeamsArchiveSource,
    TeamsArchiveTarget,
    TeamsExportOptions,
)
from office365.runtime.transport.base import BaseTransport
from requests import Response

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


def _client(transport) -> GraphClient:
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
    client = _client(_Transport(payloads))
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
