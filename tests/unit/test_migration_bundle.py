"""The bundle format: what a portable export is, and what re-reading it gives back.

A bundle is not a copy of a tree with a sidecar beside it — it is content-addressed
payloads plus one ledger, and it has to answer for itself: which destinations it
holds, which bytes each one is, and whether it is the whole export. These tests pin
that on both sides of the pair, an export and an import, without a tenant.

Deliberately not covered here: versions, permissions, authorship and the list
structure sidecar — none of them are in the format yet, and a job asked to preserve
one refuses at ``plan()`` rather than importing nothing quietly."""

from __future__ import annotations

import ast
import json
import pathlib

import pytest
from office365.migration import ConflictResolution, MigrationJob, MigrationOptions
from office365.migration.adapters.bundle import CONTENT_DIR, INDEX_NAME, LEDGER_NAME, BundleSource, BundleTarget
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners import ScanTarget
from office365.migration.base import MigrationItem
from office365.migration.offline import offline_context
from office365.migration.sharepoint import SharePointAssessmentOptions
from office365.migration.sharepoint.assessor import _ITEM_SCAN_SELECT, _UNIQUE_ITEM_SCAN_SELECT
from office365.migration.sharepoint.scanners import fields as field_scan
from office365.migration.sharepoint.scanners import lookup as lookup_scan
from office365.runtime.converters.json_file import record_to_json
from office365.runtime.limits import Limit
from office365.runtime.schema import TypeSchema
from office365.sharepoint.fields.field import Field
from office365.sharepoint.listitems.listitem import ListItem


def _index(bundle) -> dict:
    return json.loads((bundle / INDEX_NAME).read_text(encoding="utf-8"))


def _ledger_rows(bundle) -> list[dict]:
    ledger = bundle / LEDGER_NAME
    return [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]


def _blobs(bundle) -> list[str]:
    return sorted(p.name for p in (bundle / CONTENT_DIR).rglob("*") if p.is_file())


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "src"
    root.mkdir()
    (root / "a.txt").write_bytes(b"same")
    (root / "b.txt").write_bytes(b"same")
    (root / "c.txt").write_bytes(b"other")
    return root


def test_export_stores_identical_content_once_and_names_every_destination(tmp_path, source):
    bundle = tmp_path / "bundle"
    target = BundleTarget(bundle)
    job = MigrationJob(FileSystemSource(source), target)
    job.plan()
    job.run()

    assert job.stats.errors == 0
    assert sorted(target.list_paths()) == ["a.txt", "b.txt", "c.txt"]
    # "same" twice is one payload on disk, and the item count says so separately.
    assert len(_blobs(bundle)) == 2  # noqa: PLR2004 — "same" twice, "other" once
    index = _index(bundle)
    assert index["items"] == 3  # noqa: PLR2004 — three destinations
    assert index["blobs"] == 2  # noqa: PLR2004
    assert index["bytes"] == 13  # noqa: PLR2004 — 4 + 4 + 5: items, not disk
    assert index["by_type"] == {"file": 3}

    # The digest a target reports is the source's own, so a bundle is comparable.
    items = job.manifest.items
    for item in items:
        assert target.exists(item)
        assert target.checksum(item) == FileSystemSource(source).checksum(item)

    report = job.verify()
    assert report.ok and report.complete, report.summary()


def test_a_bundle_reads_back_into_another_target(tmp_path, source):
    bundle = tmp_path / "bundle"
    export = MigrationJob(FileSystemSource(source), BundleTarget(bundle))
    export.plan()
    export.run()

    imported = MigrationJob(BundleSource(bundle), FileSystemTarget(tmp_path / "dst"))
    imported.plan()
    imported.run()

    assert imported.stats.errors == 0
    assert (tmp_path / "dst" / "a.txt").read_bytes() == b"same"
    assert (tmp_path / "dst" / "c.txt").read_bytes() == b"other"
    # The import's manifest remembers what each copy is a copy *of*.
    assert {item.source_path for item in imported.manifest.items} == {
        str(source / "a.txt"),
        str(source / "b.txt"),
        str(source / "c.txt"),
    }

    report = imported.verify()
    assert report.ok and report.complete, report.summary()


def test_a_folder_is_a_ledger_row_with_no_payload(tmp_path):
    bundle = tmp_path / "bundle"
    target = BundleTarget(bundle)
    folder = MigrationItem("/srv/Empty", "Empty/", item_type="folder")
    target.write(folder, None)
    target.commit()

    assert target.list_paths() == ["Empty/"]
    assert target.exists(folder)
    assert target.checksum(folder) == ""
    with pytest.raises(IsADirectoryError):
        target.payload("Empty/")
    assert _index(bundle)["by_type"] == {"folder": 1}


def test_a_record_is_stored_in_its_json_form_and_reports_no_comparable_digest(tmp_path):
    bundle = tmp_path / "bundle"
    target = BundleTarget(bundle)
    item = MigrationItem("/list/1.json", "1", item_type="record")
    payload = {"Title": "Q3", "Amount": 12}
    target.write(item, payload)
    target.commit()

    assert target.payload("1") == payload
    blob = (bundle / CONTENT_DIR).rglob("*")
    texts = [p.read_text(encoding="utf-8") for p in blob if p.is_file()]
    assert texts == [record_to_json(payload)]
    # A record's canonical form is the record target's question, not the content's.
    assert target.checksum(item) == ""


def test_the_ledger_row_carries_what_the_next_stage_needs(tmp_path):
    target = BundleTarget(tmp_path / "bundle")
    item = MigrationItem(
        "/list/1.json",
        "1",
        item_type="record",
        modified="2026-01-05T09:30:00Z",
        created="2026-01-04T09:30:00Z",
        source_id="0f1e2d",
        metadata={"subject": "Q3 close"},
    )
    target.write(item, {"Title": "Q3"})

    row = target.row("1")
    assert row["modified"] == "2026-01-05T09:30:00Z"
    assert row["created"] == "2026-01-04T09:30:00Z"
    assert row["source_id"] == "0f1e2d"
    assert row["metadata"] == {"subject": "Q3 close"}
    assert target.modified(item) == "2026-01-05T09:30:00Z"
    assert target.row("absent") is None


def test_a_rerun_over_the_same_bundle_changes_nothing(tmp_path, source):
    bundle = tmp_path / "bundle"
    job = MigrationJob(FileSystemSource(source), BundleTarget(bundle))
    job.plan()
    job.run()
    first_rows = _ledger_rows(bundle)
    first_index = _index(bundle)
    first_index_bytes = (bundle / INDEX_NAME).read_bytes()

    again = MigrationJob(
        FileSystemSource(source),
        BundleTarget(bundle),
        options=MigrationOptions(conflict_resolution=ConflictResolution.OVERWRITE),
    )
    again.plan()
    again.run()

    assert _ledger_rows(bundle) == first_rows
    assert (bundle / INDEX_NAME).read_bytes() == first_index_bytes
    assert _index(bundle)["items"] == first_index["items"]
    assert _index(bundle)["blobs"] == first_index["blobs"]
    # The bundle keeps the moment it was started, not the moment it was re-sealed.
    assert _index(bundle)["created_at"] == first_index["created_at"]


def test_a_bundle_refuses_fidelity_it_does_not_carry(tmp_path, source):
    bundle = tmp_path / "bundle"
    export = MigrationJob(FileSystemSource(source), BundleTarget(bundle))
    export.plan()
    export.run()

    job = MigrationJob(
        BundleSource(bundle),
        BundleTarget(tmp_path / "copy"),
        options=MigrationOptions(preserve_permissions=True),
    )
    with pytest.raises(NotImplementedError):
        job.plan()


def test_the_index_is_derived_from_the_ledger(tmp_path, source):
    bundle = tmp_path / "bundle"
    target = BundleTarget(bundle)
    job = MigrationJob(FileSystemSource(source), target)
    job.plan()
    job.run()
    sealed = _index(bundle)

    (bundle / INDEX_NAME).unlink()
    reopened = BundleTarget(bundle)
    assert sorted(reopened.list_paths()) == ["a.txt", "b.txt", "c.txt"]
    assert all(reopened.exists(item) for item in job.manifest.items)

    reopened.commit()
    assert _index(bundle)["items"] == sealed["items"]
    assert _index(bundle)["blobs"] == sealed["blobs"]
    assert _index(bundle)["rollup"] == sealed["rollup"]


# What the assessment scans read, and where they read it from.
_DERIVED = {"is_file": "file_system_object_type", "is_folder": "file_system_object_type"}


_ITEM = ListItem(offline_context())


def column(**members) -> Field:
    """A column as a ``fields`` projection returns it."""
    return Field(offline_context()).hydrate(members)


def column_read(schema: TypeSchema, attr: str) -> str | None:
    """The column ``attr`` names on one type, unless it is an expanded part."""
    wire = schema.by_attr.get(attr)
    if wire is None or schema.properties[wire].navigation:
        return None
    return wire


def wire_read(node: ast.expr) -> str | None:
    """The column an ``item.<attr>`` or ``item.<navigation>.<attr>`` read asks for.

    An expanded column is spelled the way the projection spells it, ``File/Length``.
    ``None`` for a read that is not a column: a dict key, a derived kind, an expanded
    part itself, or an attribute the model does not declare.
    """
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        if node.value.id != "item":
            return None
        return column_read(ListItem._schema, _DERIVED.get(node.attr, node.attr))
    if not (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Attribute)):
        return None
    parent = node.value
    if not isinstance(parent.value, ast.Name) or parent.value.id != "item":
        return None
    part, navigation = getattr(_ITEM, parent.attr, None), ListItem._schema.by_attr.get(parent.attr)
    if part is None or navigation is None:
        return None
    wire = column_read(type(part)._schema, node.attr)
    return None if wire is None else f"{navigation}/{wire}"


def scan(scanner, entity):
    """One scan over a loaded payload."""
    report = AssessmentReport.new()
    scanner.run(ScanTarget(ScanContainer.FIELDS, entity, "web/lists/L"), report)
    return report


def test_every_column_a_scan_reads_is_in_the_projection_it_selected():
    selected = {
        "default": set(_ITEM_SCAN_SELECT),
        "unique": set(_UNIQUE_ITEM_SCAN_SELECT),
    }
    missing = []
    for path in sorted(pathlib.Path(field_scan.__file__).parent.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        load = "unique" if 'items_load = "unique"' in source else "default"
        for node in ast.walk(ast.parse(source)):
            wire = wire_read(node)
            if wire is None:
                continue
            parent = node.value
            label = f"item.{parent.attr}.{node.attr}" if isinstance(parent, ast.Attribute) else f"item.{node.attr}"
            if wire not in selected[load]:
                missing.append(f"{path.name}: {label} reads {wire}")

    assert missing == []


def test_the_lookup_scan_counts_every_family_the_column_calls_a_reference():
    columns = [
        column(InternalName="Customer", TypeAsString="Lookup"),
        column(InternalName="Owner", TypeAsString="User"),
        column(InternalName="Topics", TypeAsString="TaxonomyFieldType"),
        column(InternalName="Title", TypeAsString="Text"),
    ]

    over = scan(
        lookup_scan.LookupColumnScanner(SharePointAssessmentOptions(limits={"lookup_joins": Limit("lookup_joins", 2)})),
        columns,
    )
    at_limit = scan(
        lookup_scan.LookupColumnScanner(SharePointAssessmentOptions(limits={"lookup_joins": Limit("lookup_joins", 3)})),
        columns,
    )

    assert [issue.risk_code for issue in over.issues] == ["LIST_VIEW_LOOKUP_EXCEED_LIMIT"]
    assert at_limit.issues == []


def test_a_read_only_column_is_flagged_from_the_column_not_from_its_schema():
    columns = [
        column(InternalName="ZzLocked", ReadOnlyField=True),
        column(InternalName="ZzWritable", ReadOnlyField=False),
        column(InternalName="ZzLegacyWords", SchemaXml='<Field ReadOnly="TRUE"/>'),
    ]

    report = scan(field_scan.FieldScanner(SharePointAssessmentOptions()), columns)

    flagged = [issue.location.rsplit("/", 1)[-1] for issue in report.issues if "ReadOnly" in issue.message]
    assert flagged == ["ZzLocked"]
