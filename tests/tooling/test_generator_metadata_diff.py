"""Offline tests for comparing two metadata snapshots."""

from __future__ import annotations

from generator.metadata_diff import MemberRename, RenameCandidate, diff_metadata
from generator.odata.member import MemberInformation
from generator.odata.method import MethodInformation
from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation


def _model(*types: TypeInformation) -> ODataModel:
    model = ODataModel()
    for schema in types:
        model.add_type(schema)
    return model


def _type(name: str, *properties: str, navs: tuple[str, ...] = (), base_type: str = "") -> TypeInformation:
    schema = TypeInformation(FullName=name, BaseTypeName=base_type or None)
    for prop in properties:
        schema.add_property(PropertyInformation(Name=prop, TypeName="Edm.String"))
    for nav in navs:
        schema.add_property(PropertyInformation(Name=nav, TypeName="graph.User", IsNavigation=True))
    return schema


def _enum(name: str, **members: str) -> TypeInformation:
    schema = TypeInformation(BaseTypeFullName="EnumType", FullName=name)
    for member, value in members.items():
        schema.add_member(MemberInformation(Name=member, Value=value))
    return schema


def test_identical_snapshots_report_nothing():
    schema = _type("graph.User", "displayName")

    delta = diff_metadata(_model(schema), _model(schema), "v1", "beta")

    assert delta.is_empty
    assert delta.render() == "beta declares nothing v1 does not."


def test_a_member_the_base_declares_is_not_gained_by_re_declaring_it():
    """Beta flattens AccessPackageQuestion off Entity and declares ``id`` itself.

    ``id`` is not new: the stable root exposes it through ``Entity``. Reading declared
    members alone would call it preview-only, and a marker saying so refuses ``id`` on
    every stable request.
    """
    base = _model(
        _type("graph.Entity", "id"),
        _type("graph.AccessPackageQuestion", "text", base_type="graph.Entity"),
    )
    target = _model(
        _type("graph.Entity", "id"),
        _type("graph.AccessPackageQuestion", "id", "text"),
    )

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.is_empty


def test_a_member_that_moves_to_the_base_is_not_lost():
    """The same change seen from the other side: ``displayName`` stays reachable."""
    base = _model(
        _type("graph.Entity"),
        _type("graph.BookingBusiness", "displayName", base_type="graph.Entity"),
    )
    target = _model(
        _type("graph.Entity", "displayName"),
        _type("graph.BookingBusiness", base_type="graph.Entity"),
    )

    delta = diff_metadata(base, target, "v1", "beta")

    # The base is where the member now lives, so that is the only type that gains it.
    assert delta.properties_only_in_base == {}
    assert delta.properties_only_in_target == {"graph.Entity": ["displayName"]}


def test_suppressing_an_inherited_gain_does_not_hide_a_genuinely_new_member():
    """The suppression is about one name, not about the type's diff as a whole."""
    base = _model(
        _type("graph.Entity", "id"),
        _type("graph.AccessPackageQuestion", "text", base_type="graph.Entity"),
    )
    target = _model(
        _type("graph.Entity", "id"),
        _type("graph.AccessPackageQuestion", "id", "text", "isRequired"),
    )

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.properties_only_in_target == {"graph.AccessPackageQuestion": ["isRequired"]}


def test_a_type_only_in_the_target_is_reported_whole():
    delta = diff_metadata(
        _model(_type("graph.User", "displayName")),
        _model(_type("graph.User", "displayName"), _type("graph.BetaThing", "name")),
        "Graph.xml",
        "GraphBeta.xml",
    )

    assert delta.types_only_in_target == ["graph.BetaThing"]
    assert delta.types_only_in_base == []


def test_a_target_only_property_is_split_from_a_navigation():
    base = _model(_type("graph.User", "displayName"))
    target = _model(_type("graph.User", "displayName", "preferredLanguage", navs=("manager",)))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.properties_only_in_target == {"graph.User": ["preferredLanguage"]}
    assert delta.navigations_only_in_target == {"graph.User": ["manager"]}


def test_a_property_the_target_dropped_is_reported_separately():
    base = _model(_type("graph.User", "displayName", "legacyThing"))
    target = _model(_type("graph.User", "displayName"))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.properties_only_in_base == {"graph.User": ["legacyThing"]}
    assert delta.properties_only_in_target == {}


def test_a_renamed_property_is_one_change_not_an_addition_plus_a_loss():
    """Graph's beta renames in place: the type gains and loses at the same time."""
    base = _model(_type("graph.AccessPackage", "catalog", "displayName"))
    target = _model(_type("graph.AccessPackage", "accessPackageCatalog", "displayName"))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.renamed == [MemberRename("graph.AccessPackage", "property", "catalog", "accessPackageCatalog")]
    assert delta.properties_only_in_base == {}
    assert delta.properties_only_in_target == {}
    assert delta.rename_candidates == []


def test_a_renamed_navigation_is_paired_the_same_way():
    """``catalog`` is a navigation on ``accessPackage`` and beta renames it too."""
    base = _model(_type("graph.AccessPackage", "displayName", navs=("catalog", "resourceRoleScopes")))
    target = _model(
        _type(
            "graph.AccessPackage",
            "displayName",
            navs=("accessPackageCatalog", "accessPackageResourceRoleScopes"),
        )
    )

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.renamed == [
        MemberRename("graph.AccessPackage", "navigation", "catalog", "accessPackageCatalog"),
        MemberRename("graph.AccessPackage", "navigation", "resourceRoleScopes", "accessPackageResourceRoleScopes"),
    ]


def test_a_property_is_never_paired_with_a_navigation_of_the_same_name():
    base = _model(_type("graph.AccessPackage", "catalog"))
    target = _model(_type("graph.AccessPackage", navs=("accessPackageCatalog",)))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.renamed == []
    assert delta.properties_only_in_base == {"graph.AccessPackage": ["catalog"]}
    assert delta.navigations_only_in_target == {"graph.AccessPackage": ["accessPackageCatalog"]}


def test_a_shortened_name_is_claimed_but_a_coincidence_is_not():
    """``completedDateTime`` -> ``completedDate`` is a rename; ``name`` -> ``displayName`` is not."""
    base = _model(_type("graph.Item", "completedDateTime", "name"))
    target = _model(_type("graph.Item", "completedDate", "displayName"))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.renamed == [MemberRename("graph.Item", "property", "completedDateTime", "completedDate")]
    assert delta.properties_only_in_base == {"graph.Item": ["name"]}
    assert delta.properties_only_in_target == {"graph.Item": ["displayName"]}
    assert delta.rename_candidates == []


def test_two_equally_similar_names_are_not_paired():
    """A wrong pair rewrites a wire name the service never renamed: stay quiet."""
    base = _model(_type("graph.AccessPackage", "catalog"))
    target = _model(_type("graph.AccessPackage", "accessPackageCatalog", "betaCatalog"))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.renamed == []
    assert delta.properties_only_in_base == {"graph.AccessPackage": ["catalog"]}
    assert delta.rename_candidates == [
        RenameCandidate("graph.AccessPackage", "property", "catalog", ("accessPackageCatalog", "betaCatalog"))
    ]


def test_the_closest_of_two_candidates_wins_and_the_other_is_left_lost():
    base = _model(_type("graph.Item", "state", "assignmentState"))
    target = _model(_type("graph.Item", "assignmentState", "betaAssignmentState"))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.renamed == [MemberRename("graph.Item", "property", "state", "betaAssignmentState")]
    assert delta.properties_only_in_base == {}


def test_same_name_different_edm_type_is_a_conflict_not_an_addition():
    base_schema = TypeInformation(FullName="graph.Event")
    base_schema.add_property(PropertyInformation(Name="start", TypeName="graph.DateTimeTimeZone"))
    target_schema = TypeInformation(FullName="graph.Event")
    target_schema.add_property(PropertyInformation(Name="start", TypeName="Edm.DateTimeOffset"))

    delta = diff_metadata(_model(base_schema), _model(target_schema), "v1", "beta")

    assert delta.properties_only_in_target == {}
    assert [(c.member, c.base_type, c.target_type) for c in delta.member_type_conflicts] == [
        ("start", "graph.DateTimeTimeZone", "Edm.DateTimeOffset")
    ]


def test_enum_members_are_compared_by_name_and_by_value():
    """A beta enum can add members *and* renumber the ones already there."""
    base = _model(_enum("graph.Status", active="0", archived="1"))
    target = _model(_enum("graph.Status", active="0", archived="2", pending="3"))

    delta = diff_metadata(base, target, "v1", "beta")

    assert delta.enum_members_only_in_target == {"graph.Status": ["pending"]}
    assert [(c.member, c.base_value, c.target_value) for c in delta.enum_value_changes] == [("archived", "1", "2")]


def test_methods_are_compared_because_they_will_be_generated_one_day():
    base_schema = TypeInformation(FullName="graph.User")
    base_schema.add_method(MethodInformation(Name="getMailTips"))
    target_schema = TypeInformation(FullName="graph.User")
    target_schema.add_method(MethodInformation(Name="getMailTips"))
    target_schema.add_method(MethodInformation(Name="sendMailAsBeta"))

    delta = diff_metadata(_model(base_schema), _model(target_schema), "v1", "beta")

    assert delta.methods_only_in_target == {"graph.User": ["sendMailAsBeta"]}


def test_the_json_report_carries_every_bucket_in_full():
    base = _model(_type("graph.User", "displayName"))
    added = [f"p{index}" for index in range(20)]
    target = _model(_type("graph.User", "displayName", *added))

    payload = diff_metadata(base, target, "v1", "beta").to_dict()

    assert payload["metadata"] == {"base": "v1", "target": "beta"}
    assert payload["properties_only_in_target"]["graph.User"] == sorted(added)
