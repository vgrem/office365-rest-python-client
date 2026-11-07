"""What the assessment scans read, and where they read it from.

Two facts nothing else states. Every column a scan reads through the item model is in
the projection that scan selected -- a column left out of ``$select`` comes back absent,
so the scan under-reports without an error. And a column scan asks the ``Field`` what it
holds rather than re-deriving the answer from ``SchemaXml``.
"""

from __future__ import annotations

import ast
import pathlib

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners import ScanTarget
from office365.migration.offline import offline_context
from office365.migration.sharepoint import SharePointAssessmentOptions
from office365.migration.sharepoint.assessor import _ITEM_SCAN_SELECT, _UNIQUE_ITEM_SCAN_SELECT
from office365.migration.sharepoint.scanners import fields as field_scan
from office365.migration.sharepoint.scanners import lookup as lookup_scan
from office365.runtime.limits import Limit
from office365.runtime.schema import TypeSchema
from office365.sharepoint.fields.field import Field
from office365.sharepoint.listitems.listitem import ListItem

#: Attributes that answer *for* a row rather than being a column of it.
_DERIVED = {"is_file": "file_system_object_type", "is_folder": "file_system_object_type"}

#: A row as the walkers hand one to a scan — asked only for what an expanded part is.
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
