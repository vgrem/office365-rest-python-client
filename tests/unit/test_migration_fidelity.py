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
