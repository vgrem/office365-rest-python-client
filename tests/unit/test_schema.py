"""What a type's declarations answer at run time: its projection, its rank, its refusals.

The declarations themselves are the generator's job -- completeness is pinned in
``tests/tooling/test_generator_e2e.py``, and consistency between a declaration and the getter
it describes by ``generator/tools/declarations.py`` (``python -m generator verify``). What is
left is the half a tenant call reaches: a declaration that exists must answer the way a reader
asks, the projection must be the request the service accepts, and a feed that refuses an
option must refuse it before the round trip. The last section is the same question asked of
every model in the package at once.
"""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
from dataclasses import replace
from datetime import datetime
from typing import Dict, Iterator, Optional
from unittest import mock

import office365
import office365.runtime as runtime_package
import pytest
from office365.communications.callrecords.collection import CallRecordCollection
from office365.directory.identities.set import IdentitySet
from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.graph_client import GraphClient
from office365.migration.offline import offline_context
from office365.onedrive.driveitems.collection import DriveItemCollection
from office365.outlook.calendar.events.event import Event
from office365.outlook.mail.messages.message import Message
from office365.planner.assignment import PlannerAssignment
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_value import ClientValue
from office365.runtime.compare_check import _fields, compare_problems
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.query_capabilities import (
    QueryOptionNotSupportedError,
    QueryPropertyNotSupportedError,
    query_capabilities,
    query_capabilities_of,
)
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import odata
from office365.security.labels.retention.collection import RetentionLabelCollection
from office365.security.triggertypes.collection import RetentionEventTypeCollection
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.navigation.navigation import Navigation
from office365.sharepoint.navigation.nodes.node import NavigationNode
from office365.sharepoint.publishing.pages.page import SitePage
from office365.sharepoint.webs.web import Web

#: A node exactly as SharePoint spells one (probed live: ``$select`` of the declared columns
#: returns these nine keys and nothing else).
_NODE_PAYLOAD = {
    "Id": 1031,
    "Title": "Docs",
    "Url": "https://contoso.sharepoint.com/sites/other/Docs",
    "IsExternal": True,
    "IsVisible": False,
    "IsDocLib": False,
    "CurrentLCID": 1033,
    "ListTemplateType": 0,
    "AudienceIds": None,
}


# --- what a type offers, and what it only declares ------------------------------------


def test_a_row_says_whether_it_is_a_file_or_a_folder():
    # ``FileSystemObjectType`` declares an enum; the wire sends its number.

    def row(raw) -> ListItem:
        payload = {} if raw is None else {"FileSystemObjectType": raw}
        return ListItem(offline_context()).hydrate(payload)

    assert row(0).is_file and not row(0).is_folder
    assert row(1).is_folder and not row(1).is_file
    assert row(2).file_system_object_type == FileSystemObjectType.Web
    assert row(None).file_system_object_type == FileSystemObjectType.Invalid  # unprojected column
    assert not row(None).is_file and not row(None).is_folder  # absent is neither


def test_expansions_is_the_complement_of_columns():
    expansions = TypeSchema.of(Event).expansions
    assert "singleValueExtendedProperties" in expansions
    assert "instances" in expansions
    assert "iCalUId" not in expansions
    assert not set(expansions) & set(TypeSchema.of(Event).columns)


def test_a_column_the_service_refuses_is_declared_but_not_offered():
    """Probed live: ``$select`` answers 400 for these names, on these types.

    The declaration stays -- hydration and comparison still know the OData name -- while the
    projection leaves it out, so ``TypeSchema.columns`` is a request the service accepts
    rather than a list that happens to contain everything. The refusal is declared by the
    getter that reads the name, so it travels with the declaration: ``TemplateScope`` and the
    item's ``DisplayName`` are refused by the type that declares them, while the Shield
    flag is answered for a ``ListItem`` and refused for a list or a web.
    """
    for cls, name in (
        (SitePage, "TemplateScope"),
        (ListItem, "Client_Title"),
        (ListItem, "DisplayName"),
        (Web, "DescriptionTranslations"),
        (Web, "TitleTranslations"),
    ):
        assert cls._schema.properties[name].selectable is False
        assert name not in TypeSchema.of(cls).columns
    assert "ShieldAddRoleAssignmentPushdown" in TypeSchema.of(ListItem).columns
    assert "ShieldAddRoleAssignmentPushdown" not in TypeSchema.of(Web).columns
    assert "ShieldAddRoleAssignmentPushdown" not in TypeSchema.of(List).columns
    # The getter that reads a refused name keeps its declaration: a page row still carries it.
    assert TypeSchema.of(SitePage).name_of("template_scope") == "TemplateScope"


def test_a_securable_projects_its_flag_and_expands_its_role_assignments():
    """A securable used to name nothing but navigations, so its projection read nothing.

    ``$select`` ignores a navigation silently (probed live: a ``ListItem`` projected with
    ``RoleAssignments`` came back without one, while ``$expand`` returned 51 assignments), so
    the flag is the column that matters -- and it is the one the service assigns, which is why
    it comes back on a response and never on a request.
    """
    assert "HasUniqueRoleAssignments" in TypeSchema.of(ListItem).columns
    assert "RoleAssignments" in TypeSchema.of(ListItem).expansions
    assert "RoleAssignments" not in TypeSchema.of(ListItem).columns
    assert TypeSchema.of(ListItem).name_of("has_unique_role_assignments") == "HasUniqueRoleAssignments"


def test_a_link_the_service_will_not_follow_on_its_own_is_not_expandable():
    """Probed live: ``$expand=extensions`` is refused without a ``$filter``.

    ``ErrorGraphExtensionExpandRequiresFilter`` -- so the member is still a navigation (the
    CSDL says it is a link), but ``$expand`` cannot follow it as it stands. The filtered
    spelling stays reachable through a raw path.
    """
    assert "extensions" in Event._schema.navigations
    assert "extensions" not in TypeSchema.of(Event).expansions
    assert "attachments" in TypeSchema.of(Event).expansions


def test_a_read_only_column_never_travels_back():
    # A hydrated item is re-read once and written back somewhere else, so what the model
    # calls read-only has to leave the payload without leaving the read.
    item = ListItem(mock.MagicMock(), ResourcePath("Items"))
    item.hydrate(dict.fromkeys(ListItem._schema.readonly))
    assert item.to_json(V4JsonFormat("none")) == {}
    assert set(item.to_json()) == set(ListItem._schema.readonly)
    assert set(ListItem._schema.readonly) <= set(TypeSchema.of(ListItem).columns)


def test_a_navigation_projects_its_columns_and_expands_its_links():
    # Both bars were declared as columns, so the projection named two navigations: ``$select``
    # answers nothing for either while ``$expand`` returns both.
    assert TypeSchema.of(Navigation).columns == ("UseShared",)
    assert TypeSchema.of(Navigation).expansions == ("QuickLaunch", "TopNavigationBar")
    assert TypeSchema.of(Navigation).name_of("use_shared") == "UseShared"
    # A node's projection is the payload a read comes back with, name for name: nine keys,
    # and ``Children``/``TitleResource`` are the navigations the same read expands instead.
    assert set(TypeSchema.of(NavigationNode).columns) == set(_NODE_PAYLOAD)
    assert TypeSchema.of(NavigationNode).expansions == ("Children", "TitleResource")
    # IsVisible and IsExternal are read-only because the service owns them: probed live,
    # neither a create body nor a merge at QuickLaunch(<id>) changes either flag.
    assert {"IsVisible", "IsExternal"} <= set(NavigationNode._schema.readonly)


def test_a_web_names_itself_with_the_url_that_travels_first():
    """One address, two spellings, and the caller picks by reach.

    Three modules in ``migration`` used to loop over the pair ``("Url", "ServerRelativeUrl")``
    by name, because a caller that has to say *which site* a web is has no other way to learn
    the two spellings. The order is the declaration's, not the caller's: the address as it
    stands travels to another site collection, the path inside this one does not.
    """
    assert TypeSchema.of(Web).identities == ("Url", "ServerRelativeUrl")
    assert TypeSchema.of(ListItem).identities == ()  # an item is identified by its key, not a column


# --- what a read asks for when the caller has no opinion ------------------------------


class Widget(ClientObject):
    #: Declared first, ranked second: the class body's order is how the CSDL lists the
    #: columns, and a table leads with a name rather than with a timestamp.
    @odata(name="createdDateTime", default=2)
    @property
    def created_at(self) -> Optional[str]:
        return self.properties.get("createdDateTime", None)

    @odata(name="title", default=1)
    @property
    def title(self) -> Optional[str]:
        return self.properties.get("title", None)

    @odata(name="eTag")
    @property
    def e_tag(self) -> Optional[str]:
        return self.properties.get("eTag", None)

    @odata(name="parent", navigation=True, default=3)
    @property
    def parent(self) -> Optional["Widget"]:
        return Widget(self.context)


class Gadget(Widget):
    """Ranking a member once is enough: a subclass reads its base's columns."""


class Plain(ClientObject):
    @odata(name="config")
    @property
    def config(self) -> Optional[str]:
        return self.properties.get("config", None)


def test_a_read_asks_for_the_ranked_columns_in_rank_order():
    widget = Widget(offline_context()).select_default()
    assert widget.query_options.select == ["title", "createdDateTime"]
    # A link is not a column even when the type ranks it.
    assert TypeSchema.of(Widget).defaults == ("title", "createdDateTime")


def test_a_type_that_ranks_nothing_adds_no_projection():
    # An empty answer is a decision, not a gap to be filled with a guess.
    assert Plain(offline_context()).select_default().query_options.select == []


def test_a_collection_and_a_subclass_read_the_rank_of_the_type_they_hold():
    collection = ClientObjectCollection(offline_context(), Widget, None)
    assert collection.select_default().query_options.select == ["title", "createdDateTime"]
    assert TypeSchema.of(Gadget).defaults == TypeSchema.of(Widget).defaults


# --- what a feed refuses before the round trip ----------------------------------------


def test_call_records_declares_top_unsupported():
    capability = query_capabilities_of(CallRecordCollection)
    assert capability is not None
    assert capability.supports("filter")
    assert not capability.supports("top")
    assert not capability.supports("$Top")  # normalized


def test_retention_feeds_refuse_every_standard_option():
    """Both Purview retention feeds answer 400 to each option, so the guard runs first.

    Measured against the two endpoints rather than inferred: the bare GET is the only request
    those feeds accept, and it is gated by Purview RBAC, which is why no live test can see this.
    """
    for collection in (RetentionEventTypeCollection(GraphClient()), RetentionLabelCollection(GraphClient())):
        with pytest.raises(QueryOptionNotSupportedError) as error:
            collection.top(3)
        assert "learn.microsoft.com" in str(error.value)
        with pytest.raises(QueryOptionNotSupportedError):
            collection.filter("displayName eq 'x'")
    records = GraphClient().communications.call_records
    with pytest.raises(QueryOptionNotSupportedError):
        records.paged(20)
    with pytest.raises(QueryOptionNotSupportedError):
        records.get_all(page_size=20)


@query_capabilities(allowed={"filter", "select"})
class _FilterSelectOnly(EntityCollection):
    pass


def test_an_allow_list_guards_the_options_it_leaves_out():
    col = _FilterSelectOnly(GraphClient(), Entity)
    col.filter("id eq '1'")
    col.select(["id"])
    with pytest.raises(QueryOptionNotSupportedError):
        col.top(1)
    with pytest.raises(QueryOptionNotSupportedError):
        col.order_by("id")


@query_capabilities(unsupported={"top"}, on_unsupported="warn")
class _WarnTop(EntityCollection):
    pass


def test_warn_mode_skips_the_option_and_still_sends_the_expression():
    col = _WarnTop(GraphClient(), Entity)
    with pytest.warns(UserWarning):
        col.top(5)
    assert col.query_options.top is None

    @query_capabilities(unsupported_filter={"size"}, on_unsupported="warn")
    class _WarnProperty(EntityCollection):
        pass

    warned = _WarnProperty(GraphClient(), Entity)
    with pytest.warns(UserWarning):
        warned.filter("size gt 0")
    assert warned.query_options.filter == "size gt 0"


def test_a_declaration_that_contradicts_itself_is_refused():
    with pytest.raises(ValueError):
        query_capabilities(unsupported={"top"}, allowed={"filter"})
    with pytest.raises(ValueError):
        query_capabilities(unsupported={"top"}, on_unsupported="nope")


def test_a_filter_on_a_property_the_feed_refuses_is_refused():
    capability = query_capabilities_of(DriveItemCollection)
    assert capability is not None
    assert capability.filter_violations("size gt 0") == ("size",)
    assert capability.filter_violations("folder ne null") == ()
    assert capability.orderby_violations("size desc") == ()  # sorting by size is fine
    col = DriveItemCollection(GraphClient())
    with pytest.raises(QueryPropertyNotSupportedError):
        col.filter("size gt 0")
    col.order_by("size desc")  # allowed


# --- a declaration and the getter that reads it ---------------------------------------


def test_name_of_answers_for_an_attribute_and_refuses_an_unknown_one():
    assert TypeSchema.of(Event).name_of("ical_uid") == "iCalUId"
    assert TypeSchema.of(Message).name_of("from_") == "from"  # a reserved word, renamed by the generator
    # A naming inverse would happily answer i_cal_u_id here; the declaration knows better.
    with pytest.raises(AttributeError, match="not a declared property"):
        TypeSchema.of(Event).name_of("i_cal_u_id")


def test_a_field_declares_itself_and_a_marker_adds_direction():
    # Planner's to_json overrides existed to pop the two fields Graph fills in and rejects on
    # write. The declaration says it once, and both profiles follow it: a response carries what
    # the service said, a request cannot claim it. A dataclass field is a declaration on its
    # own -- its name is the column, its annotation is the type -- and ``odata(...)`` adds what
    # a bare field cannot state: the direction of the value.
    assignment = PlannerAssignment(
        assignedBy=IdentitySet(user=Identity(displayName="Ann", id="1")),
        assignedDateTime=datetime(2026, 3, 9, 9, 0),
        orderHint=" !",
    )
    assert set(assignment.to_json()) == {"assignedBy", "assignedDateTime", "orderHint"}
    assert assignment.to_json(V4JsonFormat("none")) == {"orderHint": " !"}

    declared = TypeSchema.of(PlannerAssignment).properties
    assert declared["assignedBy"].readonly is True
    assert declared["assignedBy"].name == "assignedBy"
    assert declared["orderHint"].readonly is False
    assert TypeSchema.of(IdentitySet).serializable == {"application", "device", "user"}


def test_a_subclass_answers_with_its_own_declarations():
    # Inherited declarations are copied, never shared, so declaring cannot leak upward.

    class Probe(Event):
        @odata(name="probeFlag", readonly=True)
        @property
        def probe_flag(self) -> bool:
            return False

    assert Probe._schema is not Event._schema
    assert Probe._schema.properties["probeFlag"].attr == "probe_flag"
    assert Probe._schema.by_attr["probe_flag"] == "probeFlag"
    assert "probeFlag" not in Event._schema.properties  # the base class is untouched
    assert "probeFlag" in TypeSchema.of(Probe).columns
    assert Event._schema.readonly < Probe._schema.readonly


def test_a_navigation_node_reads_the_flags_the_service_spells():
    """The node asked for ``isVisible``/``isExternal``; the service sends capital I.

    Probed live: every node of a real site arrived with ``IsVisible`` and ``IsExternal`` set
    and both getters answering ``None``, which made every external link a copy of an internal
    one and every hidden node a visible one.
    """
    node = NavigationNode(offline_context()).hydrate(_NODE_PAYLOAD)
    assert node.is_external is True
    assert node.is_visible is False
    assert TypeSchema.of(node).name_of("is_external") == "IsExternal"
    # A request may not send the names the service assigns -- the two flags included: a merge
    # that asks for IsVisible=False reads back True, so asking is pointless.
    assert node.to_json(V4JsonFormat("none")) == {
        "Title": "Docs",
        "Url": "https://contoso.sharepoint.com/sites/other/Docs",
        "AudienceIds": None,
    }


def test_a_navigation_node_serializes_the_tree_it_holds():
    """The model is the sidecar: a node read with its children round-trips through JSON.

    This is what makes a migration-side copy of the tree unnecessary -- ``to_json()`` is the
    document and ``hydrate()`` rebuilds it typed, one level down included.
    """
    node = NavigationNode(offline_context()).hydrate(
        dict(_NODE_PAYLOAD, Children=[{"Title": "Child page", "Url": "/sites/x/Pages/c.aspx"}])
    )
    assert node.children[0].title == "Child page"
    document = node.to_json()
    assert document["Children"] == [{"Title": "Child page", "Url": "/sites/x/Pages/c.aspx"}]
    assert document["IsVisible"] is False  # a response carries what the service said

    again = NavigationNode(offline_context()).hydrate(document)
    assert again.children[0].url == "/sites/x/Pages/c.aspx"
    assert again.is_visible is False


# --- the same questions, asked of every model at once ---------------------------------


def _package_models() -> list:
    """Every model the package defines, imported: the hand-written ones and the generated ones."""
    found: Dict[type, None] = {}
    for module in pkgutil.walk_packages(office365.__path__, "office365."):
        for member in vars(importlib.import_module(module.name)).values():
            if isinstance(member, type) and issubclass(member, (ClientObject, ClientValue)):
                found[member] = None
    return list(found)


def test_every_compare_rule_in_the_package_fits_its_field():
    # Three models declare these rules by hand today; naming them would let the fourth
    # escape, so the walk is the gate and a rule is found by the declaration itself.
    declaring = [model for model in _package_models() if any(meta.compare for _, meta, _ in _fields(model))]
    assert declaring, "the walk found no declaring model, so it proves nothing"
    assert [problem for model in declaring for problem in compare_problems(model)] == []


def _projection_problems(model: type) -> list[str]:
    """Every way the schema of ``model`` contradicts its own declarations.

    Each projection is one filtered line over ``properties``, so the checks below are the
    properties that filtering assumes: a member is projected one way or the other, a flag
    narrows a projection instead of widening it, and the index answers with the declaration
    it was built from.
    """
    schema = TypeSchema.of(model)
    columns, navigations = set(schema.columns), set(schema.navigations)
    readonly, persistable = set(schema.readonly), set(schema.persistable)
    problems: List[str] = []
    if columns & navigations:
        problems.append(f"$select and $expand both offer {sorted(columns & navigations)}")
    if not set(schema.expansions) <= navigations:
        problems.append(f"expandable but not a navigation: {sorted(set(schema.expansions) - navigations)}")
    if readonly & persistable:
        problems.append(f"read-only and persistable at once: {sorted(readonly & persistable)}")
    for facet, names in schema.facets.items():
        if not set(names) <= columns:
            problems.append(f"facet {facet} offers {sorted(set(names) - columns)}, which $select cannot name")
    for attr, name in schema.by_attr.items():
        if schema.properties.get(name) is None or schema.properties[name].attr != attr:
            problems.append(f"{attr} is indexed as {name}, which no declaration owns")
    return problems


def test_every_model_keeps_its_projections_coherent() -> None:
    # The migration layer reads these instead of keeping name lists of its own, so a name
    # offered twice (or a flag with no member to narrow) has to fail here rather than at the
    # `$select` the caller builds from it.
    problems = [f"{model.__name__}: {problem}" for model in _package_models() for problem in _projection_problems(model)]
    assert problems == []


def test_the_walk_reaches_models_with_both_kinds_of_member() -> None:
    # The rule above proves nothing unless the walk reaches models that project both, and the
    # projections mean nothing unless they are populated: one test states both facts.
    projecting = {m.__name__ for m in _package_models() if TypeSchema.of(m).columns and TypeSchema.of(m).navigations}
    assert {"ListItem", "Web", "Event"} <= projecting


def test_every_model_stores_the_schema_its_declarations_describe() -> None:
    # ``TypeSchema.of`` answers from the schema the class stored, never by scanning it again,
    # so a class that declares something and stores nothing answers every question about
    # itself with the empty schema -- silently, and in the direction of asking for less than
    # the model can carry. Only one thing can cause that now that ``ClientValue.__init_subclass__``
    # reads every class: a subclass that writes its own ``__init_subclass__`` and forgets
    # ``super()``, a one-line mistake with no symptom.
    stale = [
        f"{model.__module__}.{model.__qualname__}"
        for model in _package_models()
        if replace(TypeSchema.of(model), name=model.__name__) != TypeSchema.build(model)
    ]
    assert stale == []


def _dataclasses_under(package: object) -> Iterator[type]:
    """Every dataclass defined by ``package`` and its submodules."""
    for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):  # type: ignore[attr-defined]
        for member in vars(importlib.import_module(module_info.name)).values():
            if isinstance(member, type) and dataclasses.is_dataclass(member):
                yield member


def _unhashable_defaults(model: type) -> list[str]:
    """The fields of ``model`` whose default is an unhashable instance."""
    offenders: List[str] = []
    for declared in dataclasses.fields(model):
        if declared.default is dataclasses.MISSING or declared.default_factory is not dataclasses.MISSING:
            continue
        try:
            hash(declared.default)
        except TypeError:
            offenders.append(declared.name)
    return offenders


def test_no_runtime_dataclass_default_is_an_unhashable_instance() -> None:
    offenders = {
        f"{model.__module__}.{model.__qualname__}.{name}": "field(default_factory=...)"
        for model in _dataclasses_under(runtime_package)
        for name in _unhashable_defaults(model)
    }
    assert not offenders, (
        "these dataclass fields default to an unhashable instance, which Python 3.11 "
        f"rejects at class-creation time: {sorted(offenders)}"
    )
