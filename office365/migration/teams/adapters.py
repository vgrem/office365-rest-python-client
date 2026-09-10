"""Teams archive adapters — Teams as a first-class migration source/target.

Plug the core :class:`~office365.migration.job.MigrationJob` into Teams::

    from office365.migration import MigrationJob
    from office365.migration.teams import TeamsArchiveSource, TeamsArchiveTarget, TeamsExportOptions

    job = MigrationJob(
        TeamsArchiveSource(client, team_ids=["..."], options=TeamsExportOptions(include_files=True)),
        TeamsArchiveTarget("./backup"),
    )
    job.plan()
    job.run()
    print(job.verify().summary())

Archive layout (target convention)::

    <team-id>/team.json
    <team-id>/messages.ndjson
    <team-id>/attachments/<channel-id>/<message-id>_<content-id>.<ext>
    <team-id>/files/<channel-id>.zip
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Iterable

from office365.migration.adapters import DataSource, DataTarget
from office365.migration.base import MigrationItem
from office365.migration.teams._extract import (
    channel_messages,
    message_to_record,
    read_team,
)
from office365.migration.teams.models import TeamsExportOptions


def encode_json(payload: Any) -> bytes:
    """Canonical JSON encoding used by both the source checksum and target write."""
    return json.dumps(payload, indent=2, default=str).encode()


def encode_ndjson(records: list[dict[str, Any]]) -> bytes:
    """Canonical NDJSON encoding (one record per line)."""
    return "".join(json.dumps(record, default=str) + "\n" for record in records).encode()


def _checksum(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def _encode_payload(item: MigrationItem, payload: Any) -> bytes:
    if item.item_type == "structure":
        return encode_json(payload)
    if item.item_type == "messages":
        return encode_ndjson(payload)
    return payload


class TeamsArchiveSource(DataSource):
    """Enumerates Teams (structure, messages, attachments, files) as migration items."""

    def __init__(
        self,
        client,
        team_ids: list[str] | None = None,
        options: TeamsExportOptions | None = None,
    ) -> None:
        self._client = client
        self._team_ids = team_ids
        self._options = options or TeamsExportOptions()
        self._cache: dict[str, dict[str, Any]] = {}

    def _ids(self) -> list[str]:
        if self._team_ids is None:
            self._team_ids = [t.id for t in self._client.teams.get_all().select(["id"]).execute_query()]
        return self._team_ids

    def _data(self, team_id: str) -> dict[str, Any]:
        if team_id in self._cache:
            return self._cache[team_id]
        channels = self._client.teams[team_id].channels.get().execute_query()
        records: list[dict[str, Any]] = []
        messages: list[tuple[str, Any]] = []
        if self._options.include_messages or self._options.include_hosted_contents:
            for channel in channels:
                for message in channel_messages(channel):
                    records.append(message_to_record(message, channel.id))
                    messages.append((channel.id, message))
        self._cache[team_id] = {"channels": channels, "records": records, "messages": messages}
        return self._cache[team_id]

    def list_items(self, progress=None) -> list[MigrationItem]:
        options = self._options
        items: list[MigrationItem] = []
        for team_id in self._ids():
            data = self._data(team_id)
            items.append(
                MigrationItem(
                    source_path=f"{team_id}/team.json",
                    dest_path=f"{team_id}/team.json",
                    item_type="structure",
                )
            )
            if options.include_messages:
                items.append(
                    MigrationItem(
                        source_path=f"{team_id}/messages.ndjson",
                        dest_path=f"{team_id}/messages.ndjson",
                        item_type="messages",
                    )
                )
            if options.include_hosted_contents:
                for channel_id, message in data["messages"]:
                    for content in message.hosted_contents:
                        extension = (content.content_type or "application/octet-stream").split("/")[-1].split("+")[0]
                        rel = f"{team_id}/attachments/{channel_id}/{message.id}_{content.id}.{extension}"
                        items.append(MigrationItem(source_path=rel, dest_path=rel, item_type="attachment"))
            if options.include_files:
                for channel in data["channels"]:
                    rel = f"{team_id}/files/{channel.id}.zip"
                    items.append(MigrationItem(source_path=rel, dest_path=rel, item_type="files"))
        return items

    def read(self, item: MigrationItem) -> Any:
        team_id, _, remainder = item.source_path.partition("/")
        data = self._data(team_id)
        if item.item_type == "structure":
            return read_team(self._client, team_id, self._options, channels=data["channels"]).to_dict()
        if item.item_type == "messages":
            return data["records"]
        if item.item_type == "attachment":
            wanted = remainder.split("/", 2)[-1]
            for _channel_id, message in data["messages"]:
                for content in message.hosted_contents:
                    extension = (content.content_type or "application/octet-stream").split("/")[-1].split("+")[0]
                    if f"{message.id}_{content.id}.{extension}" == wanted:
                        return content.get_content().execute_query().value
            raise FileNotFoundError(wanted)
        if item.item_type == "files":
            channel_id = remainder.split("/")[-1][: -len(".zip")]
            channel = next(ch for ch in data["channels"] if ch.id == channel_id)
            return self._download_channel_zip(channel)
        raise ValueError(f"Unknown item type: {item.item_type}")

    def _download_channel_zip(self, channel) -> bytes:
        folder = channel.files_folder.get().execute_query()
        with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
            folder.download_folder(tmp).execute_query()
            return Path(tmp.name).read_bytes()

    def checksum(self, item: MigrationItem) -> str:
        return _checksum(_encode_payload(item, self.read(item)))


class TeamsArchiveTarget(DataTarget):
    """Writes a Teams archive to a directory (the target convention above)."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)

    def _path(self, item: MigrationItem) -> Path:
        return self._root / item.dest_path

    def exists(self, item: MigrationItem) -> bool:
        return self._path(item).exists()

    def write(self, item: MigrationItem, payload: Any) -> None:
        path = self._path(item)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_encode_payload(item, payload))

    def list_paths(self) -> Iterable[str]:
        return (p.relative_to(self._root).as_posix() for p in self._root.rglob("*") if p.is_file())

    def checksum(self, item: MigrationItem) -> str:
        return _checksum(self._path(item).read_bytes())


__all__ = [
    "TeamsArchiveSource",
    "TeamsArchiveTarget",
    "encode_json",
    "encode_ndjson",
]
