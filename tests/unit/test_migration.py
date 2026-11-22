"""A migration run: what it writes, what it is told to spend, what it can carry, and what
survives the process being killed.

Four questions about one run, which is why they are one file. A bundle is what the run leaves
on disk -- content-addressed payloads plus one ledger, able to answer for itself which
destinations it holds and whether it is the whole export. An assessment scan is what the run
read before it started, so a column the projection did not ask for is a blind spot rather than
a copy. A client is the policy the run borrows: Graph work is sent as background, SharePoint is
paced instead, because SharePoint signals load with its health score and not with the header.
And a checkpoint is what lets a second process pick up where the first one died -- which is
only true if the file is never seen truncated.

The fidelity report sits between them: it answers, before anything is written, what the
source/target pair can actually carry, and a job asked to preserve a dimension the pair does
not have refuses at ``plan()`` rather than importing nothing quietly.

Deliberately not covered: versions, permissions, authorship and the list-structure sidecar are
not in the bundle format yet; the refusal above is the honest answer until they are.
"""

from __future__ import annotations

import ast
import json
import pathlib
from typing import Optional

import pytest
from office365.graph_client import GraphClient
from office365.migration import ConflictResolution, MigrationJob, MigrationOptions, migration_client
from office365.migration.adapters.bundle import CONTENT_DIR, INDEX_NAME, LEDGER_NAME, BundleSource, BundleTarget
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners import ScanTarget
from office365.migration.base import MigrationItem, MigrationPhase
from office365.migration.checkpoint import Checkpoint
from office365.migration.fidelity import FidelityStatus, describe_fidelity
from office365.migration.manifest import Manifest
from office365.migration.offline import offline_context
from office365.migration.outlook.calendar_adapters import IcsExportTarget
from office365.migration.outlook.fidelity import CALENDAR_EXPORT_DIMENSIONS
from office365.migration.sharepoint import SharePointAssessmentOptions
from office365.migration.sharepoint.assessor import _ITEM_SCAN_SELECT, _UNIQUE_ITEM_SCAN_SELECT
from office365.migration.sharepoint.scanners import fields as field_scan
from office365.migration.sharepoint.scanners import lookup as lookup_scan
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.converters.json_file import record_to_json
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.imports import ImportCheckpoint
from office365.runtime.limits import Limit
from office365.runtime.persistence import atomic_write_json, read_json
from office365.runtime.schema import TypeSchema
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.field import Field
from office365.sharepoint.listitems.listitem import ListItem

# --- what a portable export is --------------------------------------------------------


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


# --- what an assessment scan reads ----------------------------------------------------
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


# --- what a client is told about the work it is doing ---------------------------------


PRIORITY_HEADER = "x-ms-throttle-priority"


def _header(client: ClientRuntimeContext) -> Optional[str]:
    """Read one header off the request this client would send, without sending it."""
    request = RequestOptions(url="https://contoso.example/v1.0/me")
    client.pending_request().beforeExecute(request)
    return request.headers.get(PRIORITY_HEADER)


def _unauthenticated(client: ClientRuntimeContext) -> ClientRuntimeContext:
    """Drop the hooks that would authenticate a request that is never sent."""
    client.pending_request().beforeExecute.clear()
    return client


def test_the_priority_is_the_callers_choice_and_defaults_to_background():
    assert _header(migration_client(_unauthenticated(GraphClient()))) == "low"
    assert _header(migration_client(_unauthenticated(GraphClient()), priority="high")) == "high"
    assert _header(migration_client(_unauthenticated(GraphClient()), priority=None)) is None


def test_a_sharepoint_context_is_paced_but_carries_no_graph_header():
    ctx = migration_client(_unauthenticated(ClientContext("https://contoso.sharepoint.com")))

    assert ctx.rate_limiter is not None
    assert _header(ctx) is None


def test_pacing_is_installed_unless_declined_and_the_client_comes_back():
    client = _unauthenticated(GraphClient())

    assert migration_client(client) is client, "the policy is applied to the caller's own client"
    assert client.rate_limiter is not None
    assert migration_client(_unauthenticated(GraphClient()), pace=False).rate_limiter is None


# --- what the pair can carry ----------------------------------------------------------


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


# what the pair's own hooks answer


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


# a table the product declares


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


# --- what survives a process that dies ------------------------------------------------


def _tmp_files(directory) -> list[str]:
    return [p.name for p in directory.iterdir() if p.name.endswith(".tmp")]


def test_a_save_creates_the_directories_it_needs_and_leaves_no_temp_file(tmp_path):
    target = tmp_path / "state" / "nested" / "checkpoint.json"
    atomic_write_json(target, {"ok": True})
    assert read_json(target) == {"ok": True}
    assert _tmp_files(target.parent) == []

    path = tmp_path / "manifests" / "01-docs.manifest.json"
    Manifest([MigrationItem(source_path="/a/b.txt", dest_path="b.txt", item_type="file")]).save(path)

    assert Manifest.load(path).by_dest()["b.txt"].source_path == "/a/b.txt"
    assert _tmp_files(path.parent) == []


def test_import_checkpoint_round_trip_is_atomic(tmp_path):
    path = tmp_path / "import.json"
    checkpoint = ImportCheckpoint(cursor=10, chunks=2, errors=1, signature={"format": "csv"})
    checkpoint.save(path)
    assert _tmp_files(tmp_path) == []

    restored = ImportCheckpoint.load(path)
    assert restored.cursor == 10  # noqa: PLR2004
    assert restored.chunks == 2  # noqa: PLR2004
    assert restored.signature == {"format": "csv"}
    assert restored.updated_at  # stamped on save


def test_migration_checkpoint_round_trip_is_atomic(tmp_path):
    path = tmp_path / "migration.json"
    checkpoint = Checkpoint.create(run_id="run-1")
    checkpoint.phase = MigrationPhase.RUNNING
    checkpoint.source_watermark = "2026-01-01T00:00:00Z"
    checkpoint.items["/sites/a/file.txt"] = "done"
    checkpoint.save(path)

    assert _tmp_files(tmp_path) == []
    restored = Checkpoint.load(path)
    assert restored.run_id == "run-1"
    assert restored.phase == MigrationPhase.RUNNING
    assert restored.source_watermark == "2026-01-01T00:00:00Z"
    assert restored.items == {"/sites/a/file.txt": "done"}


def test_migration_checkpoint_save_keeps_previous_on_failure(tmp_path):
    path = tmp_path / "migration.json"
    Checkpoint.create(run_id="old").save(path)

    checkpoint = Checkpoint.create(run_id="new")
    checkpoint.items = {"bad": object()}  # type: ignore[dict-item]  # not JSON-serializable

    with pytest.raises(TypeError):
        checkpoint.save(path)

    assert Checkpoint.load(path).run_id == "old"
    assert _tmp_files(tmp_path) == []
