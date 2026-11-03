"""What the OData declarations feed at run time: ``select_all()``, ``_schema``, navigations.

The declarations themselves are the generator's job -- completeness is pinned in
``tests/tooling/test_generator_e2e.py``, and consistency between a declaration and the
getter it describes by ``generator/tools/declarations.py`` (``python -m generator verify``).
What is left here is the half a tenant call reaches: a declaration that exists must
answer the way a reader asks, and the projections must be the ones the service accepts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from unittest import mock

import pytest
from office365.directory.identity_set import IdentitySet
from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.outlook.mail.messages.message import Message
from office365.planner.assignment import PlannerAssignment
from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import _ODATA_MARKER, ODataPropertyMeta, field_declarations, odata
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.navigation.navigation import Navigation
from office365.sharepoint.navigation.nodes.node import NavigationNode
from office365.sharepoint.publishing.pages.page import SitePage
from office365.sharepoint.webs.web import Web


def test_an_item_row_column_declares_that_the_metadata_is_silent():
    """A page copy reads these by name; a reader must be able to see where they live."""
    assert {"AuthorId", "EditorId", "Created", "Modified"} <= set(ListItem._schema.system)
    assert {"FileRef", "FileLeafRef"} <= set(ListItem._schema.system)
    assert {"FileLeafRef", "WikiField", "OData__ModerationStatus"} <= set(SitePage._schema.system)
    assert "Id" not in ListItem._schema.system  # the one item column the CSDL does declare
    assert "AuthorId" in ListItem.select_all()  # still a column the service answers


def test_a_row_says_whether_it_is_a_file_or_a_folder():
    """``FileSystemObjectType`` declares an enum; the wire sends its number."""
    from office365.migration.offline import offline_context
    from office365.sharepoint.files.system_object_type import FileSystemObjectType

    def row(raw) -> ListItem:
        payload = {} if raw is None else {"FileSystemObjectType": raw}
        return ListItem(offline_context()).hydrate(payload)

    assert row(0).is_file and not row(0).is_folder
    assert row(1).is_folder and not row(1).is_file
    assert row(2).file_system_object_type == FileSystemObjectType.Web
    assert row(None).file_system_object_type == FileSystemObjectType.Invalid  # unprojected column
    assert not row(None).is_file and not row(None).is_folder  # absent is neither


def test_select_all_is_the_projection_the_declarations_describe():
    columns = Event.select_all()

    assert "iCalUId" in columns  # a column whose name a snake-case guess gets wrong
    assert "id" in columns  # inherited from Entity, so the base carries a declaration too
    assert "attachments" not in columns  # a navigation property: $select would reject it
    assert "calendar" not in columns
    assert len(columns) == len(set(columns))


def test_expand_all_is_the_complement_of_select_all():
    expand_all = Event.expand_all()

    assert "singleValueExtendedProperties" in expand_all
    assert "instances" in expand_all
    assert "iCalUId" not in expand_all
    assert not set(expand_all) & set(Event.select_all())


def test_a_column_the_service_refuses_is_declared_but_not_offered():
    """Probed live: ``$select`` answers 400 for these names, and only on these types.

    The declaration stays — hydration and comparison still know the OData name — while the
    projection leaves it out, so ``select_all()`` is a request the service accepts rather
    than a list that happens to contain everything. The refusal is a type's fact: the
    Shield flag is answered for a ``ListItem`` and refused for a ``Web``, and
    ``TemplateScope`` is refused on the page entity that declares it.
    """
    for cls in (Web, List, ListItem, SitePage):
        assert cls._unselectable  # the type states what it saw refused
        assert set(cls._unselectable) <= set(cls._schema.properties)  # about names it declares
        assert not set(cls._schema.columns) & set(cls._unselectable)
    assert "ShieldAddRoleAssignmentPushdown" in Web._unselectable
    assert "ShieldAddRoleAssignmentPushdown" in ListItem.select_all()
    assert "TemplateScope" in SitePage._unselectable
    assert "TemplateScope" not in SitePage.select_all()
    # The getter that reads it keeps its declaration: a page row still carries the column.
    assert SitePage.odata_name("template_scope") == "TemplateScope"


def test_a_securable_projects_its_flag_and_expands_its_role_assignments():
    """A securable used to name nothing but navigations, so its projection read nothing.

    ``$select`` ignores a navigation silently (probed live: a ``ListItem`` projected
    with ``RoleAssignments`` came back without one, while ``$expand`` returned 51
    assignments), so the flag is the column that matters — and it is the one the service
    assigns, which is why it comes back on a response and never on a request.
    """
    assert "HasUniqueRoleAssignments" in ListItem.select_all()
    assert "RoleAssignments" in ListItem.expand_all()
    assert "RoleAssignments" not in ListItem.select_all()
    assert ListItem.odata_name("has_unique_role_assignments") == "HasUniqueRoleAssignments"


def test_a_link_the_service_will_not_follow_on_its_own_is_not_expandable():
    """Probed live: ``$expand=extensions`` is refused without a ``$filter``.

    ``ErrorGraphExtensionExpandRequiresFilter`` — so the member is still a navigation
    (the CSDL says it is a link), but ``$expand`` cannot follow it as it stands. The
    filtered spelling stays reachable through a raw path.
    """
    assert "extensions" in Event._schema.navigations
    assert "extensions" not in Event.expand_all()
    assert "attachments" in Event.expand_all()


def test_a_read_only_column_never_travels_back():
    """A hydrated item is re-read once and written back somewhere else, so what the model
    calls read-only has to leave the payload without leaving the read."""
    item = ListItem(mock.MagicMock(), ResourcePath("Items"))
    item.hydrate(dict.fromkeys(ListItem._schema.readonly))

    assert item.to_json(V4JsonFormat("none")) == {}
    assert set(item.to_json()) == set(ListItem._schema.readonly)
    assert set(ListItem._schema.readonly) <= set(ListItem.select_all())


def test_a_fact_no_consumer_enforces_is_not_accepted():
    """Five fields were carried by every declaration, set by none, read by nothing.

    ``filterable``/``sortable``/``searchable`` answer a question the product answers, not
    the member (``QueryCapabilities`` denies per product, because Graph states it in
    prose and the snapshots state nothing); ``description`` is the getter's docstring,
    written from the same OpenAPI summary; and ``nullable`` says a *request* must carry
    the member, which nothing here checks. A keyword that is accepted and ignored is a
    promise that cannot be kept, so it now raises instead.
    """
    for fact in ("filterable", "sortable", "searchable", "nullable", "description"):
        with pytest.raises(TypeError, match=fact):
            odata(name="x", **{fact: True})


def test_odata_name_answers_for_an_attribute_and_refuses_an_unknown_one():
    assert Event.odata_name("ical_uid") == "iCalUId"
    assert Message.odata_name("from_") == "from"  # a reserved word, renamed by the generator
    # A naming inverse would happily answer i_cal_u_id here; the declaration knows better.
    with pytest.raises(AttributeError, match="not a declared property"):
        Event.odata_name("i_cal_u_id")


def test_one_declaration_serves_a_property_and_a_dataclass_field():
    # A ClientValue is a dataclass, so it has fields where a ClientObject has
    # properties. The fact is the same one -- the JSON key, and who owns the value --
    # so the declaration is the same: callable for a property, a Mapping for a field.
    declaration = odata(name="assignedDateTime", readonly=True)
    assert declaration[_ODATA_MARKER].name == "assignedDateTime"
    assert declaration[_ODATA_MARKER].readonly is True

    @dataclass
    class Draft(ClientValue):
        assigned_date_time: str | None = field(default=None, metadata=odata(name="assignedDateTime"))

    declared = Draft.__dataclass_fields__["assigned_date_time"].metadata[_ODATA_MARKER]
    assert isinstance(declared, ODataPropertyMeta)
    assert declared.name == "assignedDateTime"


def test_a_nested_field_declares_who_owns_its_value():
    # Planner's to_json overrides existed to pop the two fields Graph fills in and
    # rejects on write. The declaration says it once, and both profiles follow it:
    # a response carries what the service said, a request cannot claim it.
    assignment = PlannerAssignment(
        assignedBy=IdentitySet(user=Identity(displayName="Ann", id="1")),
        assignedDateTime=datetime(2026, 3, 9, 9, 0),
        orderHint=" !",
    )
    assert set(assignment.to_json()) == {"assignedBy", "assignedDateTime", "orderHint"}
    assert assignment.to_json(V4JsonFormat("none")) == {"orderHint": " !"}


def test_declaring_a_nested_field_is_opt_in():
    declared = field_declarations(PlannerAssignment)
    assert declared["assignedBy"].readonly is True
    assert declared["assignedBy"].name == "assignedBy"
    assert "orderHint" not in declared  # undeclared fields keep their own name
    assert field_declarations(IdentitySet) == {}  # 2,887 nested types are untouched


def test_a_type_s_declarations_are_one_object_built_once():
    """Every projection a payload needs is an attribute of one class fact.

    The projections are derived, so they cannot disagree with the declarations they
    come from, and they are built when the class is created, so a module can ask the
    type without an instance (``contacts_models`` derives a replay set from
    ``Contact._schema.readonly``).
    """
    schema = Event._schema

    assert Event._schema is schema  # built once per class, not rebuilt per ask
    assert Event(None)._schema is schema  # and one answer for instances too
    assert schema.readonly == frozenset(name for name, meta in schema.properties.items() if meta.readonly)
    assert schema.columns == tuple(name for name, meta in schema.properties.items() if not meta.navigation)
    assert schema.navigations == tuple(name for name, meta in schema.properties.items() if meta.navigation)
    assert schema.by_attr["ical_uid"] == "iCalUId"  # a rename only the declaration knows
    assert "id" in Entity._schema.readonly  # inherited by every entity
    assert "id" in Contact._schema.readonly
    assert Contact._schema.persistable == frozenset()
    assert ClientObject._schema.properties == {}  # a type that declares nothing


def test_a_subclass_answers_with_its_own_declarations():
    """Inherited declarations are copied, never shared, so declaring cannot leak upward."""

    class Probe(Event):
        @odata(name="probeFlag", readonly=True)
        @property
        def probe_flag(self) -> bool:
            return False

    assert Probe._schema is not Event._schema
    assert Probe._schema.properties["probeFlag"].attr == "probe_flag"
    assert Probe._schema.by_attr["probe_flag"] == "probeFlag"
    assert "probeFlag" not in Event._schema.properties  # the base class is untouched
    assert "probeFlag" in Probe.select_all()
    assert Event._schema.readonly < Probe._schema.readonly


_NAV_CONTEXT = "https://contoso.sharepoint.com/sites/x"

#: A node exactly as SharePoint spells one (probed live: ``$select`` of the declared
#: columns returns these nine keys and nothing else).
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


def test_a_navigation_declares_one_column_and_reaches_its_bars():
    """Both bars were declared as columns, so the projection named two navigations.

    ``$select=QuickLaunch,TopNavigationBar`` answers nothing for either while
    ``$expand`` returns both, so a projection built from ``select_all()`` read one
    name and promised three.
    """
    assert Navigation.select_all() == ["UseShared"]
    assert Navigation.expand_all() == ["QuickLaunch", "TopNavigationBar"]
    assert Navigation.odata_name("use_shared") == "UseShared"


def test_a_navigation_node_projects_the_columns_a_read_returns():
    # The one declaration the node carried was TitleResource, a navigation; the
    # other ten fields were read through properties no projection could name.
    assert NavigationNode.select_all() == [
        "Id",
        "Title",
        "Url",
        "IsVisible",
        "IsExternal",
        "AudienceIds",
        "CurrentLCID",
        "IsDocLib",
        "ListTemplateType",
    ]
    assert NavigationNode.expand_all() == ["Children", "TitleResource"]
    # IsVisible and IsExternal are here because the service owns them: probed live,
    # neither a create body nor a merge at QuickLaunch(<id>) changes either flag.
    assert NavigationNode._schema.readonly == {
        "Id",
        "IsVisible",
        "IsExternal",
        "CurrentLCID",
        "IsDocLib",
        "ListTemplateType",
    }


def test_a_navigation_node_reads_the_flags_the_service_spells():
    """The node asked for ``isVisible``/``isExternal``; the service sends capital I.

    Probed live: every node of a real site arrives with ``IsVisible`` and
    ``IsExternal`` set and both getters answering ``None``, which made every external
    link a copy of an internal one and every hidden node a visible one.
    """
    node = NavigationNode(ClientContext(_NAV_CONTEXT)).hydrate(_NODE_PAYLOAD)

    assert node.is_external is True
    assert node.is_visible is False
    assert node.odata_name("is_external") == "IsExternal"
    # A request may not send the names the service assigns -- the two flags included:
    # a merge that asks for IsVisible=False reads back True, so asking is pointless.
    assert node.to_json(V4JsonFormat("none")) == {
        "Title": "Docs",
        "Url": "https://contoso.sharepoint.com/sites/other/Docs",
        "AudienceIds": None,
    }


def test_a_navigation_node_serializes_the_tree_it_holds():
    """The model is the sidecar: a node read with its children round-trips through JSON.

    This is what makes a migration-side copy of the tree unnecessary -- ``to_json()``
    is the document and ``hydrate()`` rebuilds it typed, one level down included.
    """
    node = NavigationNode(ClientContext(_NAV_CONTEXT)).hydrate(
        dict(_NODE_PAYLOAD, Children=[{"Title": "Child page", "Url": "/sites/x/Pages/c.aspx"}])
    )

    assert node.children[0].title == "Child page"
    document = node.to_json()
    assert document["Children"] == [{"Title": "Child page", "Url": "/sites/x/Pages/c.aspx"}]
    assert document["IsVisible"] is False  # a response carries what the service said

    again = NavigationNode(ClientContext(_NAV_CONTEXT)).hydrate(document)
    assert again.children[0].url == "/sites/x/Pages/c.aspx"
    assert again.is_visible is False
