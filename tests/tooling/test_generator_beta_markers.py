"""The ``beta=`` markers are derived from the snapshots, so they can also be withdrawn.

A marker that no longer describes the preview root is worse than no marker: a reader
trusts it, and a request acts on it. These tests pin the three edits a regeneration
can need -- add, change, remove -- and the source read that supplies "what the model
declares now", since the code is the state and there is no side file to drift.
"""

from __future__ import annotations

from generator.beta_markers import (
    BETA_ONLY,
    RENAMED,
    STABLE_ONLY,
    MemberMarker,
    compare_markers,
    plan_markers,
    read_declared_markers,
)
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
