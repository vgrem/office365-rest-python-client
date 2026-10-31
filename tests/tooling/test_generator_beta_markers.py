"""The ``@version(beta=...)`` gate: what the two snapshots justify, and how the plan is
written -- idempotently, and with the removal that keeps a gate the next snapshot stops
justifying from outliving it.

Two halves, one subject: :mod:`generator.beta_markers` decides, and
:func:`generator.marker_apply.apply_markers` types that decision. Nothing here touches a
network: the snapshots are built in the test and the model is source written into
``tmp_path``.
"""

from __future__ import annotations

from pathlib import Path

from generator.beta_markers import (
    BETA_ONLY,
    RENAMED,
    STABLE_ONLY,
    MarkerEdits,
    MarkerPlan,
    MemberMarker,
    VersionMarker,
    compare_markers,
    plan_markers,
    read_declared_markers,
    read_declared_versions,
)
from generator.marker_apply import TypeFiles, apply_markers
from generator.metadata_diff import diff_metadata
from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation

PREVIEW_VERSION = "beta"


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


def test_a_member_the_preview_root_dropped_is_marked_so_the_stable_client_keeps_it():
    base = _type("graph.User", "displayName", "legacyOnly")
    target = _type("graph.User", "displayName")

    plan = _plan(base, target)

    assert plan.markers == [MemberMarker("graph.User", "legacyOnly", "property", False, STABLE_ONLY)]


def test_a_model_with_no_markers_needs_them_added():
    edits = compare_markers(_plan(NOW, PREVIEW), declared={})

    assert [marker.member for marker in edits.added] == ["assignmentPolicies", "catalog", "uniqueName"]
    assert edits.changed == []
    assert edits.removed == []
    assert edits.render() == "beta markers: 3 to add, 0 to change, 0 to remove"


def test_a_marker_that_already_says_the_right_thing_is_left_alone():
    plan = _plan(NOW, PREVIEW)
    declared = {marker.key: marker.beta for marker in plan.markers}

    assert compare_markers(plan, declared).is_empty


def test_a_preview_that_adopted_the_stable_spelling_withdraws_the_marker():
    """``catalog`` renamed in beta today may stop being renamed tomorrow."""
    was = _plan(NOW, PREVIEW)
    declared = {marker.key: marker.beta for marker in was.markers}

    settled = _plan(
        NOW, _type("graph.AccessPackage", "displayName", "uniqueName", navs=("assignmentPolicies", "catalog"))
    )
    edits = compare_markers(settled, declared)

    assert edits.added == []
    assert edits.changed == []
    assert [marker.member for marker in edits.removed] == ["assignmentPolicies", "catalog"]
    assert [marker.member for marker in edits.removed if marker.reason == BETA_ONLY] == []
    assert edits.render() == "beta markers: 0 to add, 0 to change, 2 to remove"


def test_a_member_that_became_stable_loses_its_beta_only_marker():
    declared = {("graph.AccessPackage", "uniqueName"): True}

    settled = _plan(NOW, _type("graph.AccessPackage", "displayName", navs=("assignmentPolicies", "catalog")))
    edits = compare_markers(settled, declared)

    assert [marker.member for marker in edits.removed] == ["uniqueName"]


def test_a_marker_whose_name_moved_is_changed_not_readded():
    declared = {("graph.AccessPackage", "catalog"): "oldPreviewName"}

    edits = compare_markers(_plan(NOW, PREVIEW), declared)

    assert [(marker.member, marker.beta) for marker in edits.changed] == [("catalog", "accessPackageCatalog")]
    assert [marker.member for marker in edits.added] == ["assignmentPolicies", "uniqueName"]


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


def test_the_model_is_read_back_from_its_own_source():
    declared = read_declared_markers({"graph.AccessPackage": DECLARING})

    assert declared == {
        ("graph.AccessPackage", "uniqueName"): True,
        ("graph.AccessPackage", "catalog"): "accessPackageCatalog",
        ("graph.AccessPackage", "assignmentPolicies"): "accessPackageAssignmentPolicies",
    }
    assert compare_markers(_plan(NOW, PREVIEW), declared).is_empty


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


def test_the_json_report_carries_the_plan_and_the_edits(tmp_path):
    from generator.beta_markers import write_report

    plan = _plan(NOW, PREVIEW)
    path = tmp_path / "markers.json"
    write_report(plan, compare_markers(plan, {}), str(path))

    payload = path.read_text(encoding="utf-8")
    assert '"count": 3' in payload
    assert '"reason": "renamed"' in payload
    assert '"removed": []' in payload


def _plan_a_type_only_the_target_declares():
    return plan_markers(
        diff_metadata(_model(NOW), _model(PREVIEW, _type("graph.Mention", "application")), "Graph.xml", "GraphBeta.xml")
    )


def test_a_type_only_the_target_declares_is_carried_by_the_plan():
    """A member marker says "this attribute is the preview root's"; a type can be too."""
    plan = _plan_a_type_only_the_target_declares()

    assert plan.types == (VersionMarker("graph.Mention", PREVIEW_VERSION),)
    assert "1 type(s) the target alone declares" in plan.render()


def test_a_type_the_model_does_not_gate_needs_it_added():
    edits = compare_markers(_plan_a_type_only_the_target_declares(), declared={}, declared_versions={})

    assert [marker.type_name for marker in edits.types_added] == ["graph.Mention"]
    assert "1 type(s) to gate" in edits.render()


def test_a_type_that_already_states_the_right_version_is_left_alone():
    plan = _plan_a_type_only_the_target_declares()
    declared = {marker.key: marker.beta for marker in plan.markers}

    edits = compare_markers(plan, declared, declared_versions={"graph.Mention": {"beta"}})

    assert edits.is_empty


def test_a_gate_beta_stopped_justifying_leaves_the_plan():
    """Beta dropping a type, or adopting it, withdraws the gate the same way a marker is."""
    settled = plan_markers(diff_metadata(_model(NOW), _model(PREVIEW), "Graph.xml", "GraphBeta.xml"))

    edits = compare_markers(settled, declared={}, declared_versions={"graph.Mention": frozenset({"beta"})})

    assert [marker.type_name for marker in edits.types_removed] == ["graph.Mention"]
    assert "1 to ungate" in edits.render()


# ---------------------------------------------------------------------- applying


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

VALUE_SOURCE = """from dataclasses import dataclass


@dataclass
class Widget(ClientValue):
    is_mentioned: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""

BASE_SOURCE = """from office365.runtime.types.odata_property import odata


class Entity:
    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self):
        return self.properties.get("createdDateTime", None)
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


def test_a_beta_only_member_gains_its_marker(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)

    assert '@odata(name="uid", beta=True)' in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "uid")]


def test_a_navigation_is_marked_after_its_name_not_at_the_end(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("mentions", True, "navigation")], changed=[], removed=[]), tmp_path)

    assert '@odata(name="mentions", beta=True, navigation=True)' in _text(tmp_path)
    assert report.edits[0].action == "added"


def test_a_rename_carries_the_preview_spelling(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("mentions", "widgetMentions")], changed=[], removed=[]), tmp_path)

    assert '@odata(name="mentions", beta="widgetMentions", navigation=True)' in _text(tmp_path)
    assert report.edits[0].after == '@odata(name="mentions", beta="widgetMentions", navigation=True)'


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


def test_a_dry_run_reports_without_writing(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)
    before = _text(tmp_path)

    dry = apply_markers(
        MarkerEdits(added=[_marker("mentions", True)], changed=[], removed=[]), _tree(tmp_path), dry_run=True
    )

    assert not dry.is_empty
    assert _text(tmp_path) == before
    assert report.edits


def test_a_member_declared_on_a_base_class_is_marked_where_it_is_written(tmp_path):
    edits = MarkerEdits(added=[_marker("createdDateTime", True)], changed=[], removed=[])

    report = apply_markers(edits, _tree(tmp_path, widget=SOURCE, entity=BASE_SOURCE), dry_run=False)

    assert '@odata(name="createdDateTime", beta=True, readonly=True)' in _text(tmp_path, "entity")
    assert '@odata(name="uid")' in _text(tmp_path, "widget")
    assert report.edits[0].path.endswith("entity.py")


def test_a_member_no_decorator_declares_is_reported_not_guessed(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("notDeclaredAnywhere", True)], changed=[], removed=[]), tmp_path)

    assert report.edits == []
    assert report.skipped[0][1] == "no @odata(name=...) declares this member"
    assert "notDeclaredAnywhere" not in _text(tmp_path)


def test_a_method_marker_is_skipped_because_methods_are_not_generated(tmp_path):
    report = _apply(MarkerEdits(added=[_marker("markAsJunk", True, "method")], changed=[], removed=[]), tmp_path)

    assert report.edits == []
    assert "generate_methods" in report.skipped[0][1]


def test_a_preview_member_that_went_stable_loses_its_marker(tmp_path):
    """The promotion case: the plan is empty, so the declared marker has to go."""
    _apply(MarkerEdits(added=[_marker("uid", True)], changed=[], removed=[]), tmp_path)
    assert "beta=True" in _text(tmp_path)

    declared = read_declared_markers({"microsoft.graph.Widget": tmp_path / "widget.py"})
    edits = compare_markers(MarkerPlan(base="v1", target="beta", markers=[]), declared)
    report = apply_markers(edits, _tree(tmp_path), dry_run=False)

    assert {marker.member for marker in edits.removed} == {"uid", "businessPhones"}
    assert "beta=" not in _text(tmp_path)
    assert {edit.action for edit in report.edits} == {"removed"}


def test_a_rename_the_preview_adopted_is_marked_as_a_rename(tmp_path):
    _apply(MarkerEdits(added=[], changed=[], removed=[]), tmp_path)
    plan = MarkerPlan(
        base="v1",
        target="beta",
        markers=[MemberMarker("microsoft.graph.Widget", "mentions", "navigation", "widgetMentions", RENAMED)],
    )

    edits = compare_markers(plan, read_declared_markers({"microsoft.graph.Widget": tmp_path / "widget.py"}))
    apply_markers(edits, _tree(tmp_path), dry_run=False)

    assert '@odata(name="mentions", beta="widgetMentions", navigation=True)' in _text(tmp_path)
    assert "beta=" in _text(tmp_path)


def _gate() -> MarkerEdits:
    return MarkerEdits(added=[], changed=[], removed=[], types_added=[VersionMarker("microsoft.graph.Widget", "beta")])


def test_a_type_only_the_preview_root_declares_states_its_version(tmp_path):
    """The class is where the version is knowable, so the class is where the fact is written."""
    report = _apply(_gate(), tmp_path)

    assert '@version("beta")\nclass Widget(Entity):\n' in _text(tmp_path)
    assert "from office365.runtime.types.odata_property import odata, version" in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("added", "version")]
    assert read_declared_versions({"microsoft.graph.Widget": tmp_path / "widget.py"}) == {
        "microsoft.graph.Widget": frozenset({"beta"})
    }


def test_the_gate_is_written_once_even_when_the_run_repeats(tmp_path):
    _apply(_gate(), tmp_path)
    first = _text(tmp_path)

    report = _apply_again(_gate(), tmp_path)

    assert _text(tmp_path) == first
    assert report.edits == []


def test_a_gate_beta_stopped_justifying_leaves_the_class(tmp_path):
    _apply(_gate(), tmp_path)

    ungated = MarkerEdits(
        added=[], changed=[], removed=[], types_removed=[VersionMarker("microsoft.graph.Widget", "beta")]
    )
    report = _apply_again(ungated, tmp_path)

    assert "@version(" not in _text(tmp_path)
    assert "import odata\n" in _text(tmp_path)
    assert [(edit.action, edit.member) for edit in report.edits] == [("removed", "version")]


def test_a_value_type_is_not_gated_because_no_request_can_name_it(tmp_path):
    """A gate nothing enforces is a comment pretending to be a rule."""
    report = apply_markers(_gate(), _tree(tmp_path, widget=VALUE_SOURCE))

    assert "@version(" not in _text(tmp_path)
    assert "not addressed by a request" in report.skipped[0][1]


NO_DECLARATION_IMPORT = """from office365.entity import Entity


class Widget(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Widget"
"""


def test_the_import_is_written_for_a_class_that_declares_nothing_else(tmp_path):
    """A type with no properties imports no declaration module; the gate brings it in."""
    _apply(_gate(), tmp_path, widget=NO_DECLARATION_IMPORT)

    assert "from office365.entity import Entity\nfrom office365.runtime.types.odata_property import version\n" in _text(
        tmp_path
    )


def test_the_import_goes_back_out_with_the_last_gate(tmp_path):
    """An import nothing names is litter, so un-gating takes it back."""
    _apply(_gate(), tmp_path, widget=NO_DECLARATION_IMPORT)
    _apply_again(
        MarkerEdits(added=[], changed=[], removed=[], types_removed=[VersionMarker("microsoft.graph.Widget", "beta")]),
        tmp_path,
    )

    assert "odata_property" not in _text(tmp_path)
