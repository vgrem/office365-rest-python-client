"""The permission vocabulary: what the tree declares, which API answers for a name, and one aggregation.

A live run answers the first two the wrong way. A wrong permission name is refused, and the harness
reads the refusal as "not granted" - so a typo and a missing grant look the same; and a declaration
that is *missing* fails nothing anywhere, so nothing names it. The third question - whether the four
declarations about a type agree with each other - is not about the wire at all.
"""

from __future__ import annotations

from typing import Any

import office365
import pytest
from office365.capabilities import capabilities_of
from office365.communications.callrecords.collection import CallRecordCollection
from office365.directory.applications.roles.collection import AppRoleCollection
from office365.directory.applications.roles.role import AppRole
from office365.directory.permissions.checker import verify_permissions
from office365.directory.permissions.guard import has_application_permission, has_delegated_permission
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.outlook.mail.messages.message import Message
from office365.permissions import APPLICATION, DELEGATED, ResourceName, catalog, declared, index, require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.types.collections import StringCollection
from tests._scripted_transport import graph
from tests.capabilities import TenantState

CLIENT_ID = "11111111-1111-1111-1111-111111111111"

#: One walk of the tree, at import: what the library promises and where it still says nothing.
LIBRARY = index(office365)

#: Public operations that still name no permission, per service package. The map only shrinks: a
#: harvest lowers a number here, and a declaration removed anywhere raises one, which is the point -
#: a debt nobody writes down is a debt nobody pays. The detector counts a method that *submits* a
#: query (``add_query``, ``execute_query``, ``execute_batch``), so these are a floor: the real
#: number is higher, never lower. A package that publishes no product keeps no entry: its methods
#: are reached through the products that inherit them, so the ledger would be naming the filing
#: cabinet rather than the service that has to grant the permission.
#:
#: These 13 are what a fill that read one table per operation - from the docs as published - could
#: not read, and neither reason is a judgement about which permission is *right*:
#:
#: * nine name a member the REST reference publishes no operation page for, so there is no table to
#:   read - ``AccessReviewScheduleDefinition.stop``, ``AiInteractionHistory.get_all_enterprise_interactions``,
#:   ``CalendarSharingMessage.accept``, ``DeviceManagementCompliancePolicy.assign``,
#:   ``DeviceManagementConfigurationPolicy.assign``,
#:   ``DeviceManagementReports.retrieve_device_app_installation_status_report``,
#:   ``ExchangeAdminClient.invoke_all``, ``OnenotePage.onenote_patch_content``, ``OnenotePage.preview``;
#: * four are documented as ``Not supported.`` in every flow, which is the reference answering the
#:   question rather than leaving it open - ``NamedLocation.restore``, ``ConditionalAccessPolicy.restore``,
#:   ``Workflow.clear_quarantine``, ``RecoveryJobBase.cancel``.
PENDING: dict[str, int] = {
    "copilot": 1,
    "directory": 5,
    "exchange": 1,
    "intune": 3,
    "onenote": 2,
    "outlook": 1,
}


def test_an_operation_that_names_no_permission_is_a_debt_that_only_shrinks():
    """Every public method that submits a request says what the tenant must grant."""
    assert LIBRARY.debt() == PENDING, "declare the permission on the method, or record the new count"


def test_a_declared_name_is_one_the_api_publishes():
    """A name is a grant only if the API that owns it offers it, and the tree can ask.

    ``office365/permissions/snapshots`` holds the names each service principal publishes, so a
    declaration cannot outlive the permission it names.
    """
    unknown, unpublished = set(), []
    for operation in LIBRARY.declared():
        for requirement in operation.declaration.requirements():
            snapshot = catalog(requirement.resource)
            if snapshot is None:
                unknown.add(str(requirement.resource))
                continue
            for kind, names in ((DELEGATED, requirement.delegated), (APPLICATION, requirement.application)):
                unpublished += [
                    f"{requirement.resource} does not publish {kind} {name}"
                    for name in names
                    if not snapshot.publishes(name, kind)
                ]

    assert LIBRARY.declared(), "no declarations found - the index is empty, not the tree"
    assert unpublished == [], "a declaration names a permission the API does not publish"
    assert unknown == set(), "no snapshot for this API: run scripts/gen_permission_catalog.py"


@require_permission(resource=ResourceName.SharePoint, delegated=["AllSites.FullControl"])
def list_sites() -> None:
    """A SharePoint method with a SharePoint declaration; never called, only read."""


class _Grants:
    """A resource's principal: only the two reads ``guard`` makes on one."""

    def __init__(self, context, delegated: list[str], application: list[str]) -> None:
        self._context = context
        self._delegated = delegated
        self._application = application

    def get_delegated_permissions(self, app_id: str) -> ClientResult[StringCollection]:
        return ClientResult(self._context, StringCollection(self._delegated))

    def get_application_permissions(self, app_id: str) -> ClientResult[AppRoleCollection]:
        return ClientResult(self._context, AppRoleCollection([AppRole(value=value) for value in self._application]))


class _Principals:
    """The ``servicePrincipals`` collection, remembering the resource it was asked for."""

    def __init__(self, principals: dict[str, _Grants]) -> None:
        self.principals = principals
        self.asked: list[str] = []

    def find_by_name(self, name: Any, *, required: bool = False) -> _Grants:
        self.asked.append(str(name))
        return self.principals[str(name)]


def _client() -> "_Client":
    """A client whose two resources deliberately grant different things: that is the whole point."""
    return _Client()


class _Client:
    """What ``guard`` reads off a client: the principals collection, and nothing else."""

    def __init__(self) -> None:
        context = graph()[0]
        self.service_principals = _Principals(
            {
                ResourceName.Graph.value: _Grants(context, delegated=["Sites.ReadWrite.All"], application=["Mail.Send"]),
                ResourceName.SharePoint.value: _Grants(context, delegated=["AllSites.FullControl"], application=[]),
            }
        )

    @property
    def asked(self) -> list[str]:
        return self.service_principals.asked


def test_a_check_without_a_resource_reads_microsoft_graph():
    client = _client()

    assert has_delegated_permission(client, "Sites.ReadWrite.All", CLIENT_ID)
    assert client.asked == [ResourceName.Graph.value]


def test_a_check_reads_the_grants_of_the_resource_it_names():
    client = _client()

    assert has_delegated_permission(client, "AllSites.FullControl", CLIENT_ID, ResourceName.SharePoint)
    assert client.asked == [ResourceName.SharePoint.value]


def test_one_name_is_answered_per_resource_not_once_for_the_client():
    """The same name, the same client: two resources, two answers.

    Caching by resource while reading Graph's grants would have turned the second answer into the
    first one, which is the failure this pins.
    """
    client = _client()

    assert has_delegated_permission(client, "Sites.ReadWrite.All", CLIENT_ID)
    assert not has_delegated_permission(client, "Sites.ReadWrite.All", CLIENT_ID, ResourceName.SharePoint)


def test_an_application_permission_is_read_from_the_same_resource():
    client = _client()

    assert has_application_permission(client, "Mail.Send", CLIENT_ID)
    assert not has_application_permission(client, "Mail.Send", CLIENT_ID, ResourceName.SharePoint)


def test_the_state_a_requirement_is_checked_against_is_read_from_its_resource():
    client = _client()

    (requirement,) = declared(list_sites).requirements()
    state = TenantState.of(client, CLIENT_ID, requirement)

    assert state.delegated == frozenset({"AllSites.FullControl"})
    assert requirement.satisfied_by(state)
    assert client.asked == [ResourceName.SharePoint.value]


def test_a_report_names_the_resource_it_checked():
    client = _client()

    report = verify_permissions(client, list_sites, CLIENT_ID)

    assert report.resource == ResourceName.SharePoint.value
    assert report.granted_delegated == ["AllSites.FullControl"]


def test_a_collection_answers_shape_limits_and_query_rules():
    """One call answers every family for a type: shape, permissions, limits and query rules."""
    caps = capabilities_of(CallRecordCollection)

    assert caps.name == "office365.communications.callrecords.collection:CallRecordCollection"
    # A collection has no columns of its own; the columns belong to the type it collects.
    assert caps.schema.columns == ()
    assert len(caps.limits) == 4  # noqa: PLR2004
    assert not caps.queries.supports("top")
    assert "get_direct_routing_calls" in caps.declarations


def test_an_entity_answers_its_declarations_and_no_query_rules():
    caps = capabilities_of(DriveItem)

    assert len(caps.schema.columns) > 0
    assert len(caps.declarations) > 0
    assert caps.declarations["get"].application
    assert len(caps.limits) == 9  # noqa: PLR2004
    # Query rules are the collection's, and a drive item is not a collection.
    assert caps.queries is None


def test_one_call_answers_for_itself():
    caps = capabilities_of(Message.send)

    assert caps.declarations["send"].delegated == ("Mail.Send",)
    assert caps.schema is None
    assert caps.queries is None


def test_an_override_that_names_nothing_does_not_hide_the_base():
    class Base:
        @require_permission(application=["Sites.Read.All"])
        def read(self):
            """Read."""

    class Child(Base):
        def read(self):
            """Read, restated without a declaration."""

    assert capabilities_of(Child).declarations["read"].application == ("Sites.Read.All",)


def test_an_override_that_names_something_replaces_the_base():
    class Base:
        @require_permission(application=["Sites.Read.All"])
        def read(self):
            """Read."""

    class Child(Base):
        @require_permission(application=["Sites.FullControl.All"])
        def read(self):
            """Read, with its own declaration."""

    assert capabilities_of(Child).declarations["read"].application == ("Sites.FullControl.All",)


def test_licenses_are_the_union_of_the_plans_named_once_each():
    class Mixed:
        @require_permission(application=["Sites.Read.All"], licenses=["SharePoint Online"])
        def read(self):
            """Read."""

        @require_permission(delegated=["Files.Read"], licenses=["Office 365 E3", "SharePoint Online"])
        def write(self):
            """Write."""

    assert capabilities_of(Mixed).licenses == ("Office 365 E3", "SharePoint Online")


def test_a_type_that_names_nothing_is_reported_not_refused():
    caps = capabilities_of(type("Bare", (), {}))

    assert dict(caps.declarations) == {}
    assert caps.licenses == ()
    assert caps.schema.columns == ()


def test_something_that_is_neither_a_type_nor_a_call_is_refused():
    with pytest.raises(TypeError):
        capabilities_of("DriveItem")
