"""Generated getters declare their own OData metadata (name, navigation).

The OData name is a fact about the CSDL, not something derivable from the attribute
name: ``iCalUId`` and ``icalUid`` both round-trip through a snake-case guess, and
only one of them is a real column. These tests pin the declaration and the codemod
that back-filled it onto files the generator will not re-render.

Completeness is claimed for the two services whose metadata the codemod reads --
``office365/outlook`` against ``Graph.xml`` and ``office365/sharepoint`` against
``SharePoint.xml`` -- and it is claimed by running the codemod: a gate that re-spelled
the back-fill's rule would agree with itself.
"""

from __future__ import annotations

import ast
import importlib
import pathlib
import pkgutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, get_origin, get_type_hints

import pytest
from office365.communications.onlinemeetings.online_meeting_info import OnlineMeetingInfo
from office365.directory.identity_set import IdentitySet
from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.outlook.mail.messages.message import Message
from office365.planner.assignment import PlannerAssignment
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_value import ClientValue
from office365.runtime.converters.value import declared_type
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.types.odata_property import _ODATA_MARKER, ODataPropertyMeta, field_declarations, odata
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.navigation.navigation import Navigation
from office365.sharepoint.navigation.nodes.node import NavigationNode
from office365.sharepoint.publishing.pages.page import SitePage
from office365.sharepoint.webs.web import Web

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
#: Packages whose columns are expected to declare their value type today.
_SERVED = ("office365/outlook",)

_spec = importlib.util.spec_from_file_location("_mark_odata", _REPO_ROOT / "scripts" / "mark_odata.py")
assert _spec is not None and _spec.loader is not None
_mark_odata = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mark_odata)


@pytest.mark.parametrize(("service", "root"), [("graph", "office365/outlook"), ("sharepoint", "office365/sharepoint")])
def test_every_getter_that_spells_an_odata_name_declares_it(service: str, root: str) -> None:
    # A getter reads a name the CSDL knows and leaves it undeclared, so the property is
    # unselectable and unmappable. The back-fill closed that; this holds it closed.
    catalog = _mark_odata.load_catalog(service)
    index = _mark_odata.type_index(catalog)
    planned = {
        str(path.relative_to(_REPO_ROOT)): len(markers)
        for path in sorted((_REPO_ROOT / root).rglob("*.py"))
        if (markers := _mark_odata.plan_module(path, catalog, index))
    }
    assert planned == {}


_PREVIEW_GETTER = """
from office365.runtime.types.odata_property import odata


class Event:
    def entity_type_name(self):
        return "microsoft.graph.Event"

    @odata(name="uid")
    @property
    def uid(self):
        return self.properties.get("uid", None)
"""


_PER_LIST_TYPE_NAME = """
from office365.runtime.types.odata_property import odata


class TicketRow:
    def entity_type_name(self):
        return self._ticket.entity_type_name()

    @odata(name="AuthorId")
    @property
    def author_id(self):
        return self.properties.get("AuthorId", None)
"""


def _plan(tmp_path: pathlib.Path, source: str, *, service: str = "graph") -> list:
    module = tmp_path / "event.py"
    module.write_text(source, encoding="utf-8")
    catalog = _mark_odata.load_catalog(service)
    return _mark_odata.plan_module(module, catalog, _mark_odata.type_index(catalog))


_TWO_GETTERS_ONE_NAME = """
from office365.runtime.types.odata_property import odata


class Team:
    def entity_type_name(self):
        return "microsoft.graph.Team"

    @odata(name="guestSettings")
    @property
    def guest_settings(self):
        return self.properties.get("guestSettings", None)

    @property
    def messaging_settings(self):
        return self.properties.get("guestSettings", None)
"""


def test_a_wire_name_gets_one_owner(tmp_path: pathlib.Path) -> None:
    """Two declarations of one name leave ``_schema.properties[name].attr`` on the last.

    The class still holds both getters, but a name read by wire -- ``get_property``
    answers through the declared attribute -- would reach the wrong one, so the
    second getter is reported rather than declared.
    """
    module = tmp_path / "team.py"
    module.write_text(_TWO_GETTERS_ONE_NAME, encoding="utf-8")
    catalog = _mark_odata.load_catalog("graph")
    duplicates: list = []

    planned = _mark_odata.plan_module(module, catalog, _mark_odata.type_index(catalog), duplicates=duplicates)

    assert planned == []
    assert duplicates == ["Team.messaging_settings reads 'guestSettings', declared by guest_settings"]


def test_a_type_name_the_instance_decides_names_no_csdl_type(tmp_path: pathlib.Path) -> None:
    """A list item answers with its list's type per instance -- not a name to read here."""
    assert _plan(tmp_path, _PER_LIST_TYPE_NAME, service="sharepoint") == []


def test_a_member_only_the_preview_declares_is_not_a_system_column(tmp_path: pathlib.Path) -> None:
    """``system=True`` says the metadata has never heard of the name; beta has."""
    assert _plan(tmp_path, _PREVIEW_GETTER) == []


def test_the_preview_snapshot_is_in_the_checkout_and_merged() -> None:
    """The declarations this file pins are read out of the preview snapshot, so it ships.

    ``Event.uid`` is declared only by ``/beta``: the test above passes because the codemod
    merged ``GraphBeta.xml``, not because the stable root happens to name it. Keeping that
    file untracked made the guarantee local-only -- CI answered 4,019 types instead of
    8,074 and four neighbours here failed with diffs that never named the cause.
    """
    snapshot = _REPO_ROOT / "generator" / "metadata" / "GraphBeta.xml"
    assert snapshot.is_file(), f"{snapshot} is a build input, not a scratch download"
    assert _mark_odata.declared_of(_mark_odata.load_catalog("graph")["microsoft.graph.event"], "uid") is not None


def test_only_the_root_that_has_a_preview_snapshot_reads_one() -> None:
    """Graph has a ``/beta`` root; the v3 service has one document and no second spelling."""
    assert _mark_odata._PREVIEW_SNAPSHOT == {"graph": "GraphBeta.xml"}


_INHERITED_GETTER = """
from office365.runtime.types.odata_property import odata


class OnlineMeeting:
    def entity_type_name(self):
        return "microsoft.graph.OnlineMeeting"

    @odata(name="joinInformation")
    @property
    def join_information(self):
        return self.properties.get("joinInformation", None)
"""


def test_a_member_a_base_type_declares_is_not_one_the_metadata_is_silent_about(tmp_path: pathlib.Path) -> None:
    """``joinInformation`` is ``onlineMeetingBase``'s; ``system=True`` would deny it."""
    assert _plan(tmp_path, _INHERITED_GETTER) == []


_OTHER_SPELLING_GETTER = """
from office365.runtime.types.odata_property import odata


class Drive:
    def entity_type_name(self):
        return "microsoft.graph.Drive"

    @odata(name="sharepointIds")
    @property
    def sharepoint_ids(self):
        return self.properties.get("sharepointIds", None)
"""


def test_a_member_the_type_spells_otherwise_is_not_a_system_column(tmp_path: pathlib.Path) -> None:
    """``drive`` declares ``sharePointIds``; ``driveItem`` declares ``sharepointIds``.

    The getter reads the other type's spelling, so an exact lookup misses it and would
    call the member one the metadata has never heard of -- it has, and the flag is about
    the member, not about the bytes we typed. The declaration is left alone either way:
    ``navigation``/``readonly`` belong to ``sharePointIds``, not to this spelling.
    """
    assert _plan(tmp_path, _OTHER_SPELLING_GETTER) == []


def test_a_getter_that_reads_an_inherited_member_declares_it(tmp_path: pathlib.Path) -> None:
    """The same fold decides the back-fill: an inherited column is a column of this type."""
    source = _INHERITED_GETTER.replace('    @odata(name="joinInformation")\n', "")

    edits = _plan(tmp_path, source)

    assert [edit.new for edit in edits] == ['    @odata(name="joinInformation")\n']


def test_a_type_keeps_its_own_answer_for_a_member_it_inherits() -> None:
    """A redeclaration narrows: the nearest declaration wins, and a looped chain is cut."""
    own = {
        "a": {"x": _mark_odata.Declared("x", False, False, True)},
        "b": {"x": _mark_odata.Declared("x", False, False, False), "y": _mark_odata.Declared("y", False, False, True)},
        "c": {},
    }
    bases = {"a": "b", "b": "c", "c": "b"}  # c <-> b: data, not a promise

    inherited = _mark_odata._inherited("a", own, bases)

    assert inherited["x"].readonly is True  # a's own declaration, not b's
    assert inherited["y"].readonly is True


def test_a_getter_is_marked_without_re_importing_odata_beside_another_name(tmp_path: pathlib.Path) -> None:
    """``from ... import Compare, odata`` is an import of ``odata``; do not add a second."""
    source = _PREVIEW_GETTER.replace("import odata", "import Compare, odata").replace('    @odata(name="uid")\n', "")

    edits = _plan(tmp_path, source)

    assert [edit.new for edit in edits] == ['    @odata(name="uid")\n']


def _says_system(call: ast.Call) -> bool:
    """Whether the ``@odata`` call carries ``system=True``."""
    for keyword in call.keywords:
        if keyword.arg == "system":
            return bool(getattr(keyword.value, "value", True))
    return False


def _is_property(node: ast.FunctionDef) -> bool:
    return any(getattr(d, "id", "") == "property" for d in node.decorator_list if not isinstance(d, ast.Call))


@pytest.mark.parametrize(("service", "root"), [("graph", "office365/outlook"), ("sharepoint", "office365/sharepoint")])
def test_a_declaration_the_metadata_does_not_carry_says_system(service: str, root: str) -> None:
    """``system=True`` is where a name comes from, and the metadata decides.

    The CSDL describes an object graph, not a list-item row: ``SP.ListItem`` declares 24
    names and answers ``AuthorId``, ``EditorId``, ``Created``, ``Modified``, none of them
    among the 24. A declaration cannot invent that difference from memory, so the flag is
    read back against the same catalog the names came from -- in both directions, because
    a ``system`` marker on a name the metadata does declare would be as wrong.

    The catalog answers for both kinds of declaration: an absent name means the metadata
    only ever states it on some other type, and a name every subtype of this type states
    is present with ``Declared.system`` set (``generator.intrinsic_members``). Either way
    the flag is the catalog's fact, not the module's.
    """
    catalog = _mark_odata.load_catalog(service)
    index = _mark_odata.type_index(catalog)
    wrong = []
    for path in sorted((_REPO_ROOT / root).rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        if "@odata(" not in source:
            continue
        found = _mark_odata.subject(ast.parse(source), catalog, index)
        if found is None:
            continue
        for node in found.node.body:
            if not isinstance(node, ast.FunctionDef) or not _is_property(node):
                continue  # a method's ``@odata`` names a function import, not a column
            call = _mark_odata.declaration(node)
            name = _mark_odata.declared_name(call) if call is not None else None
            declared = _mark_odata.declared_of(found.properties, name or "")
            if name is not None and _says_system(call) != (declared is None or declared.system):
                wrong.append(f"{path.relative_to(_REPO_ROOT)}:{call.lineno} {found.node.name}.{name}")
    assert wrong == []


_INTRINSIC_GETTER = """
from office365.runtime.types.odata_property import odata


class ListItem:
    def entity_type_name(self):
        return "SP.ListItem"

    @property
    def file_ref(self):
        return self.properties.get("FileRef", None)
"""


def test_a_member_every_subtype_declares_is_backfilled_as_system(tmp_path: pathlib.Path) -> None:
    """``SP.ListItem`` declares 24 names; its 147 per-list subtypes each add ``FileRef``.

    The catalog answers for that kind too -- ``Declared.system``, read from
    ``generator.intrinsic_members`` -- so the back-fill declares the column instead of
    leaving it as the one bare getter in the row, and finishes a marker that is already
    there without the flag.
    """
    edits = _plan(tmp_path, _INTRINSIC_GETTER, service="sharepoint")
    assert [edit.new for edit in edits] == ['    @odata(name="FileRef", system=True)\n']

    marked = _INTRINSIC_GETTER.replace("    @property\n", '    @odata(name="FileRef")\n    @property\n')
    assert [edit.new for edit in _plan(tmp_path, marked, service="sharepoint")] == [
        '    @odata(name="FileRef", system=True)\n'
    ]


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


def _declared_kind(cls: type, name: str) -> Optional[str]:
    """``"object"`` or ``"value"`` from a getter's annotation, ``None`` when unresolvable."""
    prop = getattr(cls, name, None)
    if not isinstance(prop, property) or prop.fget is None:
        return None
    try:
        hint = get_type_hints(prop.fget).get("return")
    except Exception:  # a TYPE_CHECKING-only import cannot be resolved at runtime
        return None
    target = get_origin(hint) or hint
    if not isinstance(target, type):
        return None
    return "object" if issubclass(target, (ClientObject, ClientObjectCollection)) else "value"


def test_a_declared_member_is_a_navigation_exactly_when_its_type_is_a_client_object():
    """A link and a value are already separated by their base type.

    So ``navigation`` is not a second fact to maintain: it is that separation spelled
    where the class body can read it, and the CSDL agrees with the annotation by
    construction. Where the annotation does not resolve (a ``TYPE_CHECKING``-only
    import) there is nothing to compare, so the member is skipped — but every listed type
    must still resolve enough to be checked, so the rule cannot quietly stop applying.
    """
    checked_types = (Event, Message, Contact, ListItem, Navigation, NavigationNode)
    disagreements, covered = [], set()
    for cls in checked_types:
        for attr, name in cls._schema.by_attr.items():
            kind = _declared_kind(cls, attr)
            if kind is None:
                continue
            covered.add(cls)
            declared = cls._schema.properties[name]
            if (kind == "object") != bool(declared.navigation):
                disagreements.append(f"{cls.__name__}.{attr}: {kind}, navigation={declared.navigation}")
    assert disagreements == []
    assert covered == set(checked_types)


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


def test_a_column_the_service_assigns_never_travels_back():
    item = ListItem(ClientContext("https://contoso.sharepoint.com/sites/x"))
    item.set_property("HasUniqueRoleAssignments", True)
    item.set_property("ID", 7)

    assert item.to_json(V4JsonFormat("none")) == {"ID": 7}  # a request may not carry it
    assert item.to_json()["HasUniqueRoleAssignments"] is True  # a response reports it
    assert item.has_unique_role_assignments is True


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


def test_no_served_module_has_a_column_without_a_declared_type():
    # A $select answers only the columns it names, so a column whose type does not
    # resolve hydrates a bare dict where the model promises a value object.
    untyped = []
    for root in _SERVED:
        package = root.replace("/", ".")
        for info in pkgutil.walk_packages([str(_REPO_ROOT / root)], prefix=f"{package}."):
            module = importlib.import_module(info.name)
            for cls in _entity_types(module):
                for name in cls.select_all():
                    if declared_type(cls, name) is None:
                        untyped.append(f"{cls.__module__}.{cls.__name__}.{name}")
    assert untyped == []


def _entity_types(module):
    for member in vars(module).values():
        if isinstance(member, type) and issubclass(member, ClientObject) and member.__module__ == module.__name__:
            yield member


def test_a_nested_column_declares_the_type_its_getter_returns():
    # These getters construct the type at runtime but used to leave the return
    # annotation off, so a declared column resolved to None.
    assert declared_type(Event, "start") is DateTimeTimeZone
    assert declared_type(Event, "end") is DateTimeTimeZone
    assert declared_type(Event, "onlineMeeting") is OnlineMeetingInfo
    assert declared_type(Event, "attendees") is not None


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
