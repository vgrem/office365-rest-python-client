"""The decorators the snapshots justify: ``@version(beta=...)`` and ``@key(...)``.

Both are derived from a metadata pair and applied to source that already exists, so
both have the same three obligations -- add what the plan says, change what moved,
remove what the snapshots stopped justifying -- and the same failure mode when the
third is forgotten: a decorator a reader trusts and a request acts on."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from generator.beta_markers import (
    BETA_ONLY,
    RENAMED,
    MarkerEdits,
    MemberMarker,
    VersionMarker,
    compare_markers,
    plan_markers,
    read_declared_markers,
)
from generator.entity_keys import KeyMarker, plan_keys
from generator.marker_apply import TypeFiles, apply_keys, apply_markers
from generator.metadata_diff import diff_metadata
from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation


def _model(*types: TypeInformation) -> ODataModel:
    model = ODataModel()
    for schema in types:
        model.add_type(schema)
    return model


def _type(name: str, *properties: str, navs: tuple[str, ...] = ()) -> TypeInformation:
    schema = TypeInformation(FullName=name)
    for prop in properties:
        schema.add_property(PropertyInformation(Name=prop, TypeName="Edm.String"))
    for nav in navs:
        schema.add_property(PropertyInformation(Name=nav, TypeName="graph.User", IsNavigation=True))
    return schema


def _plan(base: TypeInformation, target: TypeInformation):
    return plan_markers(diff_metadata(_model(base), _model(target), "Graph.xml", "GraphBeta.xml"))


NOW = _type("graph.AccessPackage", "displayName", navs=("assignmentPolicies", "catalog"))
PREVIEW = _type(
    "graph.AccessPackage",
    "displayName",
    "uniqueName",
    navs=("accessPackageAssignmentPolicies", "accessPackageCatalog"),
)
DECLARING = """
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AccessPackage(Entity):
    @odata(name="uniqueName", beta=True)
    @property
    def unique_name(self):
        return self.properties.get("uniqueName", None)

    @odata(name="catalog", beta="accessPackageCatalog", navigation=True)
    @property
    def catalog(self):
        return AccessPackageCatalog(self.context, ResourcePath("catalog", self.resource_path))

    @odata(name="assignmentPolicies", beta="accessPackageAssignmentPolicies", navigation=True)
    @property
    def assignment_policies(self):
        return AccessPackageAssignmentPolicyCollection(self.context)

    @odata(name="displayName")
    @property
    def display_name(self):
        return self.properties.get("displayName", None)
"""
SOURCE = """from office365.runtime.types.odata_property import odata


class Widget(Entity):
    @odata(name="uid")
    @property
    def uid(self) -> Optional[str]:
        return self.properties.get("uid", None)

    @odata(name="mentions", navigation=True)
    @property
    def mentions(self):
        return self.properties.get("mentions", None)

    @odata(name="businessPhones", beta=False)
    @property
    def business_phones(self):
        return self.properties.get("businessPhones", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""


def _tree(tmp_path: Path, **files: str) -> TypeFiles:
    for name, source in files.items():
        (tmp_path / f"{name}.py").write_text(source, encoding="utf-8")
    return TypeFiles(tmp_path)


def _apply(edits: MarkerEdits, tmp_path: Path, **files: str):
    files = files or {"widget": SOURCE}
    return apply_markers(edits, _tree(tmp_path, **files))


def _apply_again(edits: MarkerEdits, tmp_path: Path):
    """Apply to the tree as it stands: the seeding helper would reset the file."""
    return apply_markers(edits, TypeFiles(tmp_path))


def _marker(member: str, beta, kind: str = "property") -> MemberMarker:
    return MemberMarker("microsoft.graph.Widget", member, kind, beta, BETA_ONLY)


def _text(tmp_path: Path, name: str = "widget") -> str:
    return (tmp_path / f"{name}.py").read_text(encoding="utf-8")


def _gate() -> MarkerEdits:
    return MarkerEdits(added=[], changed=[], removed=[], types_added=[VersionMarker("microsoft.graph.Widget", "beta")])


NO_DECLARATION_IMPORT = """from office365.entity import Entity


class Widget(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""
KEY_SOURCE = """from office365.entity import Entity
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


def _key_model(**types: tuple) -> SimpleNamespace:
    """A model stand-in: only ``types`` is read, and only two fields of each type."""
    return SimpleNamespace(
        types={
            f"microsoft.graph.{name}": TypeInformation(FullName=f"microsoft.graph.{name}", IsValueObject=True, Key=key)
            for name, key in types.items()
        }
    )


def _key_tree(tmp_path, **files: str) -> TypeFiles:
    for name, source in files.items():
        (tmp_path / f"{name}.py").write_text(source, encoding="utf-8")
    return TypeFiles(tmp_path)


def _key_plan(model, files, **kwargs):
    return plan_keys(model, files, metadata="Graph.xml", **kwargs)


def _key_apply(plan, files, **kwargs):
    return apply_keys(plan, files, **kwargs)


def _key_text(tmp_path, name: str = "widget") -> str:
    return (tmp_path / f"{name}.py").read_text(encoding="utf-8")


def test_a_marker_is_derived_from_the_snapshots_never_asserted():
    plan = _plan(NOW, PREVIEW)

    assert plan.markers == [
        MemberMarker(
            "graph.AccessPackage", "assignmentPolicies", "navigation", "accessPackageAssignmentPolicies", RENAMED
        ),
        MemberMarker("graph.AccessPackage", "catalog", "navigation", "accessPackageCatalog", RENAMED),
        MemberMarker("graph.AccessPackage", "uniqueName", "property", True, BETA_ONLY),
    ]
    assert plan.render() == "GraphBeta.xml markers: 3 total -- 1 beta-only, 2 renamed, 0 stable-only"


def test_a_marker_whose_name_moved_is_changed_not_readded():
    declared = {("graph.AccessPackage", "catalog"): "oldPreviewName"}

    edits = compare_markers(_plan(NOW, PREVIEW), declared)

    assert [(marker.member, marker.beta) for marker in edits.changed] == [("catalog", "accessPackageCatalog")]
    assert [marker.member for marker in edits.added] == ["assignmentPolicies", "uniqueName"]


def test_a_snapshot_that_stops_justifying_everything_withdraws_every_marker():
    """The preview root drops a member and adopts a spelling: the file must follow."""
    declared = read_declared_markers({"graph.AccessPackage": DECLARING})
    settled = _plan(NOW, _type("graph.AccessPackage", "displayName", navs=("assignmentPolicies", "catalog")))

    edits = compare_markers(settled, declared)

    assert edits.added == []
    assert edits.changed == []
    assert [(marker.member, marker.beta) for marker in edits.removed] == [
        ("assignmentPolicies", "accessPackageAssignmentPolicies"),
        ("catalog", "accessPackageCatalog"),
        ("uniqueName", True),
    ]


def test_a_beta_only_member_gains_its_marker(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)

    assert '@odata(name="uid", beta=True)' in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "uid")]


def test_a_marker_that_changed_is_replaced_not_stacked(tmp_path):
    report = _apply(MarkerEdits(added=[], changed=[_marker("businessPhones", True)], removed=[]), tmp_path)

    assert '@odata(name="businessPhones", beta=True)' in _text(tmp_path)
    assert _text(tmp_path).count("beta=") == 1
    assert [edit.action for edit in report.edits] == ["changed"]


def test_a_marker_the_snapshots_stop_justifying_is_removed(tmp_path):
    report = _apply(MarkerEdits(added=[], changed=[], removed=[_marker("businessPhones", False)]), tmp_path)

    assert '@odata(name="businessPhones")' in _text(tmp_path)
    assert "beta=" not in _text(tmp_path)
    assert [edit.action for edit in report.edits] == ["removed"]


def test_the_second_run_is_a_no_op(tmp_path):
    edits = MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[])
    _apply(edits, tmp_path)

    again = apply_markers(edits, _tree(tmp_path), dry_run=False)

    assert again.edits == []
    assert again.is_empty


def test_the_import_goes_back_out_with_the_last_gate(tmp_path):
    """An import nothing names is litter, so un-gating takes it back."""
    _apply(_gate(), tmp_path, widget=NO_DECLARATION_IMPORT)
    _apply_again(
        MarkerEdits(added=[], changed=[], removed=[], types_removed=[VersionMarker("microsoft.graph.Widget", "beta")]),
        tmp_path,
    )

    assert "odata_property" not in _text(tmp_path)


def test_a_key_that_differs_from_the_default_is_a_marker(tmp_path):
    plan = _key_plan(_key_model(Widget=("appId",)), _key_tree(tmp_path, widget=KEY_SOURCE))

    assert plan.markers == [KeyMarker("microsoft.graph.Widget", "appId")]
    assert plan.skipped == []


def test_a_composite_key_is_refused_by_name(tmp_path):
    plan = _key_plan(_key_model(Widget=("appId", "tenantId")), _key_tree(tmp_path, widget=KEY_SOURCE))

    assert plan.markers == []
    assert "single path segment" in plan.skipped[0][1]


def test_the_decorator_lands_above_the_class_and_shares_the_import(tmp_path):
    files = _key_tree(tmp_path, widget=KEY_SOURCE)

    report = _key_apply(_key_plan(_key_model(Widget=("appId",)), files), files)

    assert "from office365.runtime.types.odata_property import key, odata" in _key_text(tmp_path)
    assert '\n@key("appId")\nclass Widget(Entity):' in _key_text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "key")]


def test_a_key_that_changed_replaces_its_decorator(tmp_path):
    """Two keys the class spells, one the snapshot moved between them: replace, never stack."""
    files = _key_tree(tmp_path, widget=WIRE_SOURCE)
    _key_apply(_key_plan(_key_model(Widget=("appId",)), files), files)
    assert '@key("appId")' in _key_text(tmp_path)

    report = _key_apply(_key_plan(_key_model(Widget=("tenantId",)), TypeFiles(tmp_path)), TypeFiles(tmp_path))

    assert '@key("tenantId")\nclass Widget' in _key_text(tmp_path)
    assert _key_text(tmp_path).count("@key(") == 1
    assert [(edit.action, edit.before, edit.after) for edit in report.edits] == [
        ("changed", '@key("appId")', '@key("tenantId")')
    ]


def test_a_key_the_snapshot_stops_justifying_is_removed(tmp_path):
    files = _key_tree(tmp_path, widget=KEY_SOURCE)
    _key_apply(_key_plan(_key_model(Widget=("appId",)), files), files)
    assert '@key("appId")' in _key_text(tmp_path)

    report = _key_apply(_key_plan(_key_model(Widget=("id",)), TypeFiles(tmp_path)), TypeFiles(tmp_path))

    assert "@key(" not in _key_text(tmp_path)
    assert "from office365.runtime.types.odata_property import odata\n" in _key_text(tmp_path)
    assert [edit.action for edit in report.edits] == ["removed"]
    assert report.edits[0].before == '@key("appId")'
