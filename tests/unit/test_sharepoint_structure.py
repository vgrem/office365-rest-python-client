"""The SharePoint list-structure snapshot: capture, round-trip, web-scope gaps.

The snapshot is read off a real ``List`` (its properties, ``Fields``, ``ContentTypes``
with their field links, and ``Views`` with their columns) over a ``RoutingTransport``
that scripts what the service answers. Only the answers are scripted — the reads
themselves are the library's.
"""

from __future__ import annotations

import json
from pathlib import Path

from office365.migration.sharepoint.structure import (
    ListStructure,
    capture_list_structure,
    compare_web_scope_structure,
    save_list_structure,
)
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.type import FieldType
from tests import test_site_url
from tests._scripted_transport import RoutingTransport

_LIST_SETTINGS = {
    "BaseTemplate": 100,
    "BaseType": 0,
    "Description": "A list",
    "ContentTypesEnabled": True,
    "EnableVersioning": True,
    "MajorVersionLimit": 50,
    "EnableModeration": False,
    "DraftVersionVisibility": 0,
    "EnableAttachments": True,
    "ReadSecurity": 1,
    "WriteSecurity": 1,
    "ValidationFormula": "",
    "ValidationMessage": "",
}

_PROJECT_SCHEMA = (
    '<Field Type="Choice" Name="ProjectType" SourceID="origin" Version="1">'
    "<CHOICES><CHOICE>Internal</CHOICE><CHOICE>External</CHOICE></CHOICES></Field>"
)


def _field(internal_name: str, **extra) -> dict:
    return {"__metadata": {"type": "SP.Field"}, "InternalName": internal_name, "Hidden": False, **extra}


def _results(*items) -> dict:
    return {"d": {"results": list(items)}}


def _context(*routes) -> tuple[ClientContext, RoutingTransport]:
    transport = RoutingTransport(list(routes))
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport
    return ctx, transport


def _source(*routes) -> tuple[ClientContext, RoutingTransport]:
    """A context whose ``Tasks`` list answers with the given per-collection routes."""
    return _context(
        *routes,
        ("/Fields", _results(_field("_ModerationStatus", FromBaseType=True, CanBeDeleted=False))),
        ("/ContentTypes", _results()),
        ("/views", _results()),
        ("lists/GetByTitle", {"d": {"Title": "Tasks", **_LIST_SETTINGS}}),
    )


def test_capture_reads_the_metadata_and_the_recreatable_columns():
    ctx, transport = _source(
        (
            "/Fields",
            _results(
                _field("_ModerationStatus", FromBaseType=True, CanBeDeleted=False),
                _field(
                    "ProjectType",
                    Title="Project Type",
                    FieldTypeKind=FieldType.Choice.value,
                    TypeAsString="Choice",
                    SchemaXml=_PROJECT_SCHEMA,
                    Required=True,
                    Group="Custom Columns",
                    Description="Kind of project",
                ),
                _field("Editor", Hidden=True),
            ),
        )
    )
    sp_list = ctx.web.lists.get_by_title("Tasks")

    structure = capture_list_structure(sp_list)

    assert (structure.title, structure.base_template, structure.base_type) == ("Tasks", 100, 0)  # noqa: PLR2004
    assert structure.content_types_enabled is True
    assert structure.settings["MajorVersionLimit"] == 50  # noqa: PLR2004
    # framework, built-in and hidden columns are the target's problem, not the copy's
    assert [f.internal_name for f in structure.fields] == ["ProjectType"]
    (project,) = structure.fields
    assert project.field_type_kind == FieldType.Choice.value
    assert project.type_as_string == "Choice"
    assert project.required is True
    assert (project.group, project.description) == ("Custom Columns", "Kind of project")
    # the schema is replayed through CreateFieldAsXml: the source's identity goes
    assert "SourceID" not in project.schema_xml
    assert "Version" not in project.schema_xml
    assert "External" in project.schema_xml
    # the columns are asked for by name, so a column the capture does not want is never read
    assert any("$select=" in url and "SchemaXml" in url for url in transport.calls)


def test_the_snapshot_round_trips_through_json(tmp_path: Path):
    ctx, _ = _source(
        (
            "/Fields",
            _results(_field("ProjectType", FieldTypeKind=FieldType.Text.value, SchemaXml='<Field Name="ProjectType"/>')),
        ),
        # a content type's links and a view's columns hang off their collection's url,
        # so the more specific route comes first
        ("/FieldLinks", _results({"FieldInternalName": "Title"}, {"FieldInternalName": "ProjectType"})),
        # the service wraps the column names in a page, as it does every collection
        ("/ViewFields", {"d": {"Items": {"results": ["Title"]}}}),
        ("/ContentTypes", _results({"StringId": "0x0100abc", "Name": "Project", "Hidden": False})),
        ("/views", _results({"Title": "All Items", "RowLimit": 30, "Hidden": False, "PersonalView": False})),
    )
    structure = capture_list_structure(ctx.web.lists.get_by_title("Tasks"))

    restored = ListStructure.from_dict(json.loads(json.dumps(structure.to_dict())))

    assert restored == structure
    # a link to a column the migration cannot recreate (`Title` is built in) is not replayed
    assert restored.content_types[0].field_internal_names == ["ProjectType"]
    assert restored.views[0].field_internal_names == ["Title"]

    path = tmp_path / "Documents.structure.json"
    save_list_structure(structure, path)
    assert ListStructure.from_dict(json.loads(path.read_text())) == structure


def test_compare_names_the_web_scope_definitions_the_target_lacks():
    source, _ = _context(
        ("/Fields", _results(_field("Region"), _field("Cost Centre"))),
        ("/ContentTypes", _results({"StringId": "0x0100ABCDEF0123456789", "Name": "Contract"})),
    )
    target, _ = _context(("/Fields", _results(_field("Region"))), ("/ContentTypes", _results()))

    missing = compare_web_scope_structure(source.web, target.web)

    assert missing.columns == ["Cost Centre"]
    assert missing.content_types == ["Contract"]
    assert missing.is_empty is False
