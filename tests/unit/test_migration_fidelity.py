"""What a migration claims to preserve, and what the pair it claims it for can actually do.

``describe_fidelity`` answers two questions from the same pair: which *requested* flags the
adapters provide, and a matrix over every dimension anyone models. Nothing here is a stand-in
adapter — the reference filesystem pair is the probe's subject, and a product's own table is
read off a real export target, so a claim and the code that makes it are never the same object.
"""

from __future__ import annotations

import json

import pytest
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.base import MigrationOptions
from office365.migration.fidelity import FidelityStatus, describe_fidelity
from office365.migration.outlook.calendar_adapters import IcsExportTarget
from office365.migration.outlook.fidelity import CALENDAR_EXPORT_DIMENSIONS

PROBE_DIMENSIONS = {
    "content",
    "versions",
    "timestamps",
    "authorship",
    "permissions",
    "attachments",
    "structure",
    "content_types",
    "typed_values",
    "item_state",
    "views",
    "navigation",
    "site_settings",
    "sharing_links",
}


@pytest.fixture
def pair(tmp_path):
    """The reference pair: one directory to another, every optional hook absent."""
    return FileSystemSource(tmp_path / "from"), FileSystemTarget(tmp_path / "to")


# --- the probe ---------------------------------------------------------------------


def test_the_reference_pair_answers_for_every_dimension_without_asking_the_tenant(pair) -> None:
    source, target = pair
    report = describe_fidelity(source, target, MigrationOptions())

    # A dimension nobody models is the one that gets silently dropped, so the set is exact.
    assert set(report.dimensions) == PROBE_DIMENSIONS
    assert report.dimensions["content"] == FidelityStatus.DELIVERED.value
    # A tree copy carries neither history nor state; shipping and sharing are not adapter work.
    for name in ("versions", "timestamps", "authorship", "permissions", "typed_values", "item_state", "views"):
        assert report.dimensions[name] == FidelityStatus.UNSUPPORTED.value
    # These are reachable by another verb, so the pair is honest rather than empty.
    for name in ("navigation", "site_settings"):
        assert report.dimensions[name] == FidelityStatus.BEST_EFFORT.value


def test_a_reason_is_kept_for_what_is_not_delivered_and_only_for_that(pair) -> None:
    source, target = pair
    report = describe_fidelity(source, target, MigrationOptions())

    assert set(report.dimension_notes) == {
        name for name, status in report.dimensions.items() if status != FidelityStatus.DELIVERED.value
    }
    assert "content" not in report.dimension_notes


def test_a_requested_flag_the_pair_cannot_carry_is_the_run_refusing_it(pair) -> None:
    source, target = pair
    report = describe_fidelity(
        source, target, MigrationOptions(preserve_versions=True, preserve_permissions=True, preserve_timestamps=True)
    )

    assert not report.ok
    assert report.unsupported == ["timestamps", "permissions", "versions"]
    assert len(report.notes) == len(report.unsupported)  # each one says what it would need
    assert "apply_timestamps" in report.notes[0]
    assert report.not_requested == ["authorship"]  # asked for nothing, so said to be off


def test_the_report_survives_json_and_says_itself_in_one_line(pair) -> None:
    source, target = pair
    report = describe_fidelity(source, target, MigrationOptions())

    assert json.loads(json.dumps(report.to_dict()))["dimensions"] == report.dimensions
    assert f"content={FidelityStatus.DELIVERED.value}" in report.matrix_summary()
    assert report.summary() == "not requested: timestamps, permissions, authorship, versions"


# --- a table the product declares ---------------------------------------------------


def test_a_product_that_names_its_own_dimensions_is_not_probed(tmp_path) -> None:
    """A mailbox has no views and no sharing links, so the SharePoint probe would say both.

    The export target carries the calendar's table, and the engine reads it instead of
    answering fourteen questions about a product this pair has nothing to do with.
    """
    report = describe_fidelity(FileSystemSource(tmp_path), IcsExportTarget(tmp_path), MigrationOptions())

    assert report.dimensions == {name: status.value for name, (status, _) in CALENDAR_EXPORT_DIMENSIONS.items()}
    assert "views" not in report.dimensions
    # The declared table keeps a reason where it is not delivered: that is the sentence a caller reads.
    assert set(report.dimension_notes) <= set(CALENDAR_EXPORT_DIMENSIONS)
    assert all(
        name in report.dimension_notes
        for name, (status, reason) in CALENDAR_EXPORT_DIMENSIONS.items()
        if status is not FidelityStatus.DELIVERED and reason
    )
