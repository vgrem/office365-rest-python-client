"""``@key(...)`` is derived from one snapshot, and refused wherever it would be a guess.

Two halves, and the tests split the same way: :func:`generator.entity_keys.plan_keys`
decides which types may be decorated (and explains every type it refuses), and
:func:`generator.marker_apply.apply_keys` types that decision -- idempotently, and with
the removal that keeps a key the next snapshot stops stating from outliving it.

Nothing here touches a network or a live service: the CSDL is five lines of XML and the
model is whatever source the test writes into ``tmp_path``.
"""

from __future__ import annotations

from types import SimpleNamespace
from xml.etree import ElementTree as ET

import pytest
from generator.entity_keys import KeyMarker, plan_keys
from generator.marker_apply import TypeFiles, apply_keys
from generator.odata.csdl import CsdlDocument
from generator.odata.type_information import TypeInformation
from generator.services import get_service

_NAMESPACES = {
    "xmlns": "http://docs.oasis-open.org/odata/ns/edm",
    "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
}


def _entity(fragment: str = "") -> ET.Element:
    return ET.fromstring(
        f'<EntityType Name="Widget" xmlns="http://docs.oasis-open.org/odata/ns/edm">{fragment}</EntityType>'
    )


def _parse(fragment: str) -> CsdlDocument:
    return CsdlDocument(ET.fromstring(fragment), _NAMESPACES)


# --------------------------------------------------------------------------- parsing


def test_a_key_is_read_in_declaration_order():
    node = _entity('<Key><PropertyRef Name="appId" /><PropertyRef Name="tenantId" /></Key>')

    assert _parse("<Edmx xmlns='http://docs.oasis-open.org/odata/ns/edm' />").parse_entity_key(node) == (
        "appId",
        "tenantId",
    )


def test_a_type_that_states_no_key_states_nothing():
    """Most derived types state none: they inherit ``entity``'s, which is not the same as having none."""
    assert _parse("<Edmx xmlns='http://docs.oasis-open.org/odata/ns/edm' />").parse_entity_key(_entity()) == ()


# --------------------------------------------------------------------------- planning

SOURCE = """from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Widget(Entity):
    @odata(name="appId")
    @property
    def app_id(self):
        return self.properties.get("appId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""

UNDECLARED_SOURCE = """from office365.entity import Entity


class Widget(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""

WIRE_SOURCE = """from office365.entity import Entity


class Widget(Entity):
    @property
    def tenant_id(self):
        return self.properties.get("tenantId", None)

    @property
    def app_id(self):
        return self.properties.get("appId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""

OVERRIDE_SOURCE = """from office365.entity import Entity


class Widget(Entity):
    @property
    def property_ref_name(self):
        return "appId"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""


def _model(**types: tuple) -> SimpleNamespace:
    """A model stand-in: only ``types`` is read, and only two fields of each type."""
    return SimpleNamespace(
        types={
            f"microsoft.graph.{name}": TypeInformation(FullName=f"microsoft.graph.{name}", IsValueObject=True, Key=key)
            for name, key in types.items()
        }
    )


def _tree(tmp_path, **files: str) -> TypeFiles:
    for name, source in files.items():
        (tmp_path / f"{name}.py").write_text(source, encoding="utf-8")
    return TypeFiles(tmp_path)


def _plan(model, files, **kwargs):
    return plan_keys(model, files, metadata="Graph.xml", **kwargs)


def test_a_key_that_differs_from_the_default_is_a_marker(tmp_path):
    plan = _plan(_model(Widget=("appId",)), _tree(tmp_path, widget=SOURCE))

    assert plan.markers == [KeyMarker("microsoft.graph.Widget", "appId")]
    assert plan.skipped == []


def test_the_default_key_is_a_fact_about_the_base_class_not_a_marker(tmp_path):
    """``@key("id")`` would restate the fallback, so the plan says so and writes nothing."""
    plan = _plan(_model(Widget=("id",)), _tree(tmp_path, widget=SOURCE))

    assert plan.markers == []
    assert plan.defaults == ["microsoft.graph.Widget"]


def test_a_composite_key_is_refused_by_name(tmp_path):
    plan = _plan(_model(Widget=("appId", "tenantId")), _tree(tmp_path, widget=SOURCE))

    assert plan.markers == []
    assert "single path segment" in plan.skipped[0][1]


def test_a_key_no_member_spells_is_refused(tmp_path):
    plan = _plan(_model(Widget=("tenantId",)), _tree(tmp_path, widget=SOURCE))

    assert plan.markers == []
    assert "no member of Widget is spelled tenantId" in plan.skipped[0][1]


def test_a_key_a_class_reads_by_wire_name_is_accepted(tmp_path):
    """Half the tree is still ``properties.get("name")``; the marker is no less true there."""
    plan = _plan(_model(Widget=("tenantId",)), _tree(tmp_path, widget=WIRE_SOURCE))

    assert plan.markers == [KeyMarker("microsoft.graph.Widget", "tenantId")]


def test_a_class_that_states_its_own_key_is_reported_not_overwritten(tmp_path):
    """The code is the state: a hand-written override is the same fact, not a conflict to win."""
    plan = _plan(_model(Widget=("tenantId",)), _tree(tmp_path, widget=OVERRIDE_SOURCE))

    assert plan.markers == []
    assert "states its key in property_ref_name" in plan.skipped[0][1]


def test_a_type_with_no_class_is_skipped(tmp_path):
    plan = _plan(_model(Missing=("appId",)), _tree(tmp_path, widget=SOURCE))

    assert plan.markers == []
    assert plan.skipped[0][1] == "no class declares this type"


def test_a_complex_type_is_out_of_scope_rather_than_refused(tmp_path):
    """The plan is about entity types; a complex type stating a key is not a marker to argue about."""
    model = _model(Widget=("appId",))
    model.types["microsoft.graph.Widget"].IsValueObject = False

    plan = _plan(model, _tree(tmp_path, widget=SOURCE))

    assert plan.markers == []
    assert plan.skipped == []


def test_the_plan_narrows_to_the_named_types(tmp_path):
    model = _model(Widget=("appId",), Thing=("tenantId",))
    files = _tree(tmp_path, widget=SOURCE, thing=SOURCE.replace("Widget", "Thing"))

    plan = plan_keys(model, files, metadata="Graph.xml", only=["Graph.WIDGET"])

    assert [marker.type_name for marker in plan.markers] == ["microsoft.graph.Widget"]
    assert plan.markers[0].key == "appId"


# --------------------------------------------------------------------------- applying


def _apply(plan, files, **kwargs):
    return apply_keys(plan, files, **kwargs)


def _text(tmp_path, name: str = "widget") -> str:
    return (tmp_path / f"{name}.py").read_text(encoding="utf-8")


def test_the_decorator_lands_above_the_class_and_shares_the_import(tmp_path):
    files = _tree(tmp_path, widget=SOURCE)

    report = _apply(_plan(_model(Widget=("appId",)), files), files)

    assert "from office365.runtime.types.odata_property import key, odata" in _text(tmp_path)
    assert '\n@key("appId")\nclass Widget(Entity):' in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "key")]


def test_the_decorator_sits_below_the_version_gate(tmp_path):
    """Stacked facts stack outwards: the gate refuses a root, the key decides an address."""
    files = _tree(tmp_path, widget=SOURCE.replace("\nclass Widget", '\n@version("beta")\nclass Widget'))

    _apply(_plan(_model(Widget=("appId",)), files), files)

    assert '@version("beta")\n@key("appId")\nclass Widget' in _text(tmp_path)


def test_a_class_with_no_declaration_gets_the_import_whole(tmp_path):
    files = _tree(tmp_path, widget=WIRE_SOURCE)

    _apply(_plan(_model(Widget=("appId",)), files), files)

    assert "from office365.runtime.types.odata_property import key\n" in _text(tmp_path)


def test_the_second_run_is_a_no_op(tmp_path):
    files = _tree(tmp_path, widget=SOURCE)
    plan = _plan(_model(Widget=("appId",)), files)
    _apply(plan, files)

    again = _apply(plan, TypeFiles(tmp_path))

    assert again.edits == []
    assert again.is_empty


def test_a_key_that_changed_replaces_its_decorator(tmp_path):
    """Two keys the class spells, one the snapshot moved between them: replace, never stack."""
    files = _tree(tmp_path, widget=WIRE_SOURCE)
    _apply(_plan(_model(Widget=("appId",)), files), files)
    assert '@key("appId")' in _text(tmp_path)

    report = _apply(_plan(_model(Widget=("tenantId",)), TypeFiles(tmp_path)), TypeFiles(tmp_path))

    assert '@key("tenantId")\nclass Widget' in _text(tmp_path)
    assert _text(tmp_path).count("@key(") == 1
    assert [(edit.action, edit.before, edit.after) for edit in report.edits] == [
        ("changed", '@key("appId")', '@key("tenantId")')
    ]


def test_a_key_the_snapshot_stops_justifying_is_removed(tmp_path):
    files = _tree(tmp_path, widget=SOURCE)
    _apply(_plan(_model(Widget=("appId",)), files), files)
    assert '@key("appId")' in _text(tmp_path)

    report = _apply(_plan(_model(Widget=("id",)), TypeFiles(tmp_path)), TypeFiles(tmp_path))

    assert "@key(" not in _text(tmp_path)
    assert "from office365.runtime.types.odata_property import odata\n" in _text(tmp_path)
    assert [edit.action for edit in report.edits] == ["removed"]
    assert report.edits[0].before == '@key("appId")'


def test_a_dry_run_reports_without_writing(tmp_path):
    files = _tree(tmp_path, widget=SOURCE)
    before = _text(tmp_path)

    report = _apply(_plan(_model(Widget=("appId",)), files), TypeFiles(tmp_path), dry_run=True)

    assert report.edits
    assert _text(tmp_path) == before


# --------------------------------------------------------------------------- refusing to write


def test_sharepoint_keys_are_reported_but_never_written():
    """613 stated keys, 271 of them unusable: a blind write would break addressing."""
    from generator.cli import key_pass
    from generator.config import ConfigError

    assert get_service("graph").keys_authoritative is True
    assert get_service("sharepoint").keys_authoritative is False
    with pytest.raises(ConfigError, match="reported rather than written"):
        key_pass("sharepoint", apply=True)
