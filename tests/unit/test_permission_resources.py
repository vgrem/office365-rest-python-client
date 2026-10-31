"""Which API's grants a permission name is checked against.

``Sites.ReadWrite.All`` is granted on Microsoft Graph, and ``Sites.ReadWrite.All`` is granted on
SharePoint: two grants, two service principals, two sets of endpoints. A check that named only the
name would be answered by Microsoft Graph - so a granted SharePoint permission would be reported
missing, and a missing one granted. These tests pin the probe to the resource the declaration
names, with a client whose two resources deliberately grant different things.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest import TestCase, mock

from office365.directory.permissions.checker import verify_permissions
from office365.directory.permissions.guard import (
    _cached_app_permissions,
    _cached_delegated_permissions,
    has_application_permission,
    has_delegated_permission,
)
from office365.graph_client import GraphClient
from office365.permissions import ResourceName, declared, require_permission
from tests.capabilities import TenantState

CLIENT_ID = "11111111-1111-1111-1111-111111111111"


@dataclass(frozen=True)
class FakeRole:
    """Just enough of an ``AppRole`` to be checked by name: its ``value``."""

    value: str


class FakeResult:
    """Just enough of a ``ClientResult``: ``execute_query()`` returns itself, carrying ``value``."""

    def __init__(self, value: list[Any]) -> None:
        self.value = value

    def execute_query(self) -> Any:
        return self


class FakePrincipal:
    """A resource's service principal, which knows only the grants made on its own resource."""

    def __init__(self, delegated: list[str], application: list[str]) -> None:
        self.delegated = delegated
        self.application = application

    def get_delegated_permissions(self, client_id: str) -> FakeResult:
        return FakeResult(list(self.delegated))

    def get_application_permissions(self, client_id: str) -> FakeResult:
        return FakeResult([FakeRole(value) for value in self.application])


class FakePrincipals:
    """The ``servicePrincipals`` collection, remembering the resource it was asked for."""

    def __init__(self, principals: dict[str, FakePrincipal]) -> None:
        self.principals = principals
        self.asked: list[str] = []

    def find_by_name(self, name: Any, *, required: bool = False) -> FakePrincipal:
        self.asked.append(str(name))
        return self.principals[str(name)]


class FakeClient:
    """A client whose Graph and SharePoint grants differ, which is the point of the whole test."""

    def __init__(self) -> None:
        self.service_principals = FakePrincipals(
            {
                ResourceName.Graph.value: FakePrincipal(delegated=["Sites.ReadWrite.All"], application=["Mail.Send"]),
                ResourceName.SharePoint.value: FakePrincipal(delegated=["AllSites.FullControl"], application=[]),
            }
        )


@require_permission(resource=ResourceName.SharePoint, delegated=["AllSites.FullControl"])
def list_sites() -> None:
    """A SharePoint method with a SharePoint declaration; never called, only read."""


class TestTheResourceOfACheck(TestCase):
    def setUp(self) -> None:
        self.client = FakeClient()

    def test_a_check_without_a_resource_reads_microsoft_graph(self):
        self.assertTrue(has_delegated_permission(self.client, "Sites.ReadWrite.All", CLIENT_ID))
        self.assertEqual(self.client.service_principals.asked, [ResourceName.Graph.value])

    def test_a_check_reads_the_grants_of_the_resource_it_names(self):
        self.assertTrue(
            has_delegated_permission(self.client, "AllSites.FullControl", CLIENT_ID, ResourceName.SharePoint)
        )
        self.assertEqual(self.client.service_principals.asked, [ResourceName.SharePoint.value])

    def test_one_name_is_answered_per_resource_not_once_for_the_client(self):
        """The same name, the same client: two resources, two answers.

        Caching by resource while reading Graph's grants would have made the second answer the
        first one, which is the failure this pins.
        """
        graph = has_delegated_permission(self.client, "Sites.ReadWrite.All", CLIENT_ID)
        sharepoint = has_delegated_permission(self.client, "Sites.ReadWrite.All", CLIENT_ID, ResourceName.SharePoint)

        self.assertTrue(graph)
        self.assertFalse(sharepoint)

    def test_an_application_permission_is_read_from_the_same_resource(self):
        self.assertTrue(has_application_permission(self.client, "Mail.Send", CLIENT_ID))
        self.assertFalse(has_application_permission(self.client, "Mail.Send", CLIENT_ID, ResourceName.SharePoint))

    def test_the_state_a_requirement_is_checked_against_is_read_from_its_resource(self):
        (requirement,) = declared(list_sites).requirements()

        state = TenantState.of(self.client, CLIENT_ID, requirement)

        self.assertEqual(state.delegated, frozenset({"AllSites.FullControl"}))
        self.assertTrue(requirement.satisfied_by(state))
        self.assertEqual(self.client.service_principals.asked, [ResourceName.SharePoint.value])

    def test_a_report_names_the_resource_it_checked(self):
        report = verify_permissions(self.client, list_sites, CLIENT_ID)

        self.assertEqual(report.resource, ResourceName.SharePoint.value)
        self.assertEqual(report.granted_delegated, ["AllSites.FullControl"])


class TestTheResourceOfTheCache(TestCase):
    """The two lookups are memoised per resource, so a stale answer cannot cross resources."""

    def tearDown(self) -> None:
        for cached in (_cached_app_permissions, _cached_delegated_permissions):
            cached.cache_clear()

    def test_a_cached_answer_belongs_to_the_resource_it_was_read_from(self):
        client = FakeClient()

        graph = _cached_delegated_permissions(client, CLIENT_ID, ResourceName.Graph)
        sharepoint = _cached_delegated_permissions(client, CLIENT_ID, ResourceName.SharePoint)

        self.assertEqual(list(graph), ["Sites.ReadWrite.All"])
        self.assertEqual(list(sharepoint), ["AllSites.FullControl"])


class _RecordingPrincipal:
    """A service principal that records the calls made on it and holds one app role."""

    def __init__(self, asked: list[str], granted: list[tuple[str, str]], resource: str) -> None:
        self.asked = asked
        self.granted = granted
        self.resource = resource

    def get_application_permissions(self, app_id: str) -> FakeResult:
        return FakeResult([FakeRole(value="Sites.FullControl.All")])

    def grant_application_permissions(self, app_id: str, name: Any) -> FakeResult:
        self.granted.append((app_id, str(name)))
        return FakeResult([])


class _RecordingPrincipals:
    """The ``servicePrincipals`` collection: what is asked for, and on which resource."""

    def __init__(self) -> None:
        self.asked: list[str] = []
        self.granted: list[tuple[str, str]] = []

    def find_by_name(self, name: Any, *, required: bool = False) -> _RecordingPrincipal:
        self.asked.append(str(name))
        return _RecordingPrincipal(self.asked, self.granted, str(name))


class TestTheClientTheWizardGrantsWith(TestCase):
    """`python -m tests.setup --grant` reaches a resource through the client's own helpers.

    The plan names the resource, so the helper must pass it on: without it the wizard would
    report a SharePoint gap and grant it to Graph, which is a different permission with a
    deceptively similar name.
    """

    def setUp(self) -> None:
        self.principals = _RecordingPrincipals()
        self.client = GraphClient(tenant="contoso.onmicrosoft.com")
        patcher = mock.patch.object(
            GraphClient, "service_principals", new_callable=mock.PropertyMock, return_value=self.principals
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(_cached_app_permissions.cache_clear)

    def test_a_grant_names_the_resource_and_reaches_its_principal(self):
        self.client.grant_application_permissions("app-id", "Sites.FullControl.All", resource=ResourceName.SharePoint)

        self.assertEqual(self.principals.asked, [ResourceName.SharePoint.value])
        self.assertEqual(self.principals.granted, [("app-id", "Sites.FullControl.All")])

    def test_a_check_names_the_resource_and_reads_its_grants(self):
        granted = self.client.has_application_permissions(
            "Sites.FullControl.All", "app-id", resource=ResourceName.SharePoint
        )

        self.assertTrue(granted)
        self.assertEqual(self.principals.asked, [ResourceName.SharePoint.value])
