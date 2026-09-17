"""Tests for migration metadata capture and honest fidelity guards."""

from __future__ import annotations

import datetime

import pytest
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.base import MigrationItem, MigrationOptions, item_from_dict, item_to_dict
from office365.migration.runner import _assert_fidelity_supported
from office365.runtime.converters.scalars import iso_or_none


def test_iso_or_none():
    assert iso_or_none(None) is None
    assert iso_or_none(datetime.datetime.min) is None  # SharePoint "not loaded" sentinel
    assert iso_or_none(datetime.datetime(2020, 1, 2, 3, 4, 5)) == "2020-01-02T03:04:05"


def test_migration_item_metadata_round_trips():
    item = MigrationItem(
        "src",
        "dst",
        created="2020-01-01T00:00:00",
        modified="2021-01-01T00:00:00",
        author_id=1,
        editor_id=2,
    )

    restored = item_from_dict(item_to_dict(item))

    assert restored.created == "2020-01-01T00:00:00"
    assert restored.modified == "2021-01-01T00:00:00"
    assert restored.author_id == 1
    assert restored.editor_id == 2  # noqa: PLR2004


def test_fidelity_flags_raise_instead_of_silently_noop():
    for flag in ("preserve_timestamps", "preserve_permissions", "preserve_versions"):
        with pytest.raises(NotImplementedError, match=flag):
            _assert_fidelity_supported(MigrationOptions(**{flag: True}))

    _assert_fidelity_supported(MigrationOptions())  # defaults are honest no-ops


def test_filesystem_source_captures_timestamps(tmp_path):
    (tmp_path / "a.txt").write_text("hi", encoding="utf-8")

    items = FileSystemSource(tmp_path).list_items()

    assert items[0].modified
    assert items[0].created


def test_watermark_skips_stale_and_advances():
    from office365.migration.checkpoint import Checkpoint
    from office365.migration.runner import _Watermark

    checkpoint = Checkpoint.create()
    watermark = _Watermark(checkpoint)
    assert watermark.value is None

    old = MigrationItem("s", "d1", modified="2020-01-01T00:00:00")
    new = MigrationItem("s", "d2", modified="2021-01-01T00:00:00")

    assert not watermark.is_stale(old)
    watermark.advance(old)
    assert checkpoint.source_watermark == "2020-01-01T00:00:00"
    assert watermark.is_stale(old)  # at the watermark -> already migrated
    assert not watermark.is_stale(new)

    watermark.advance(new)
    assert checkpoint.source_watermark == "2021-01-01T00:00:00"


class _Source:
    def __init__(self, items: list[MigrationItem]) -> None:
        self._items = items

    def list_items(self, progress=None):
        return list(self._items)

    def read(self, item):
        return b"data"

    def checksum(self, item):
        return ""

    def close(self):
        pass


class _Target:
    def __init__(self) -> None:
        self.written: list[str] = []

    def exists(self, item):
        return False

    def write(self, item, payload):
        self.written.append(item.dest_path)

    def list_paths(self):
        return list(self.written)

    def checksum(self, item):
        return ""

    def close(self):
        pass


def test_incremental_run_uses_watermark():
    from office365.migration.checkpoint import Checkpoint
    from office365.migration.runner import MigrationRunner

    source = _Source([MigrationItem("s", "a", modified="2020-01-01T00:00:00")])
    target = _Target()
    runner = MigrationRunner()

    first = Checkpoint.create()
    runner.run(source, target, source.list_items(), MigrationOptions(incremental=True), first)
    assert target.written == ["a"]
    assert first.source_watermark == "2020-01-01T00:00:00"

    # a fresh checkpoint carrying the watermark skips the unchanged item
    second = Checkpoint.create()
    second.source_watermark = first.source_watermark
    runner.run(source, target, source.list_items(), MigrationOptions(incremental=True), second)
    assert target.written == ["a"]  # nothing re-written

    # a newer item is migrated and advances the watermark
    source._items.append(MigrationItem("s", "b", modified="2021-01-01T00:00:00"))
    runner.run(source, target, source.list_items(), MigrationOptions(incremental=True), second)
    assert target.written == ["a", "b"]
    assert second.source_watermark == "2021-01-01T00:00:00"
