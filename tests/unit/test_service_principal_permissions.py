"""The service principal's permission readers must see every grant, not the first page.

Both readers used to read a relationship the tenant builds incrementally:

* assignments came from ``$expand=appRoleAssignedTo``, and Graph returns a single truncated
  page for an expanded collection (21 of one tenant's 43 roles), so a resource with many
  grants reported a subset -- and ``appRoleAssignedTo`` accepts no ``$filter`` at all, so the
  fix had to read the relationship from the client's side instead;
* delegated scopes came from the *first* grant found for the resource, so a tenant-wide grant
  hid every per-user grant (and the other way round).

Everything downstream believed the answer: skip decisions in live tests, permission reports,
and the "already granted" check that makes granting idempotent.
"""

from __future__ import annotations

from typing import Any

from office365.graph_client import GraphClient
from office365.permissions import ResourceName
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from tests._scripted_transport import RoutingTransport

RESOURCE_SP = "11111111-1111-1111-1111-111111111111"
CLIENT_SP = "22222222-2222-2222-2222-222222222222"
OTHER_SP = "33333333-3333-3333-3333-333333333333"
# assignments are read from the client's side; a grant is written to the resource's side
ASSIGNMENTS = f"/servicePrincipals/{CLIENT_SP}/appRoleAssignments"
GRANTS = f"/servicePrincipals/{RESOURCE_SP}/appRoleAssignedTo"

GRAPH_SP = {
    "id": RESOURCE_SP,
    "displayName": ResourceName.Graph,
    "appRoles": [
        {"id": "r1", "value": "Mail.Read", "displayName": "Mail.Read", "isEnabled": True},
        {"id": "r2", "value": "Mail.ReadWrite", "displayName": "Mail.ReadWrite", "isEnabled": True},
        {"id": "r3", "value": "Mail.Send", "displayName": "Mail.Send", "isEnabled": True},
    ],
}


def _assignment(app_role_id: str, principal_id: str = CLIENT_SP) -> dict[str, Any]:
    return {"id": f"a-{app_role_id}", "appRoleId": app_role_id, "principalId": principal_id, "resourceId": RESOURCE_SP}


def _grant(resource_id: str, consent_type: str, scope: str) -> dict[str, Any]:
    return {
        "id": f"g-{resource_id}-{consent_type}-{scope.replace(' ', '_')}",
        "clientId": CLIENT_SP,
        "resourceId": resource_id,
        "consentType": consent_type,
        "scope": scope,
    }


def _client(
    assignment_pages: list[list[dict[str, Any]]] | None = None,
    grants: list[dict[str, Any]] | None = None,
) -> tuple[GraphClient, RoutingTransport]:
    """A Graph client whose assignment list is served one page at a time."""
    transport: RoutingTransport

    def _assignments(request: RequestOptions) -> dict[str, Any]:
        if request.method != HttpMethod.Get:  # a create/delete of one assignment, not a listing
            return {}
        reads = [r for r in transport.requests if "appRoleAssignments" in r.url and r.method == HttpMethod.Get]
        page = len(reads) - 1
        body: dict[str, Any] = {"value": assignment_pages[page] if assignment_pages else []}
        if assignment_pages and page + 1 < len(assignment_pages):
            body["@odata.nextLink"] = f"https://graph.microsoft.com/v1.0{ASSIGNMENTS}?$skiptoken={page + 2}"
        return body

    transport = RoutingTransport(
        [
            (ASSIGNMENTS, _assignments),
            (GRANTS, {"id": "new-assignment"}),
            ("oauth2PermissionGrants", {"value": grants or []}),
            ("appId=", {"id": CLIENT_SP}),
            ("servicePrincipals", {"value": [GRAPH_SP]}),
        ]
    )
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def _resource(client: GraphClient) -> Any:
    return client.service_principals.find_by_name(ResourceName.Graph, required=True)


def _requests(transport: RoutingTransport, method: HttpMethod) -> list[RequestOptions]:
    return [request for request in transport.requests if request.method == method]


def test_every_assigned_role_is_reported_across_pages() -> None:
    client, transport = _client([[_assignment("r1")], [_assignment("r2"), _assignment("r3")]])

    granted = _resource(client).get_application_permissions("app").execute_query().value

    assert sorted(role.value for role in granted) == ["Mail.Read", "Mail.ReadWrite", "Mail.Send"]
    assert "skiptoken=2" in transport.requests[-1].url  # the second page was read


def test_the_assignments_are_asked_for_by_resource_on_the_server() -> None:
    client, transport = _client([[_assignment("r1")]])

    _resource(client).get_application_permissions("app").execute_query()

    request = next(r for r in transport.requests if "appRoleAssignments" in r.url)
    assert "resourceId" in request.url
    assert RESOURCE_SP in request.url
    assert "$expand" not in request.url


def test_a_resource_with_no_assignments_reports_nothing() -> None:
    client, _ = _client([[]])

    granted = _resource(client).get_application_permissions("app").execute_query().value

    assert list(granted) == []


def test_granting_a_held_role_is_a_no_op() -> None:
    client, transport = _client([[_assignment("r1")]])

    _resource(client).grant_application_permissions("app", "Mail.Read").execute_query()

    assert _requests(transport, HttpMethod.Post) == []


def test_granting_an_unheld_role_posts_it_once() -> None:
    client, transport = _client([[]])

    _resource(client).grant_application_permissions("app", "Mail.Read").execute_query()

    posts = _requests(transport, HttpMethod.Post)
    assert len(posts) == 1
    assert posts[0].url.endswith("/appRoleAssignedTo")
    assert "r1" in str(posts[0].data)


def test_revoking_a_held_role_deletes_that_assignment_only() -> None:
    client, transport = _client([[_assignment("r1"), _assignment("r2")]])

    _resource(client).revoke_application_permissions("app", "Mail.Read").execute_query()

    deletes = _requests(transport, HttpMethod.Delete)
    assert len(deletes) == 1
    assert "a-r1" in deletes[0].url


def test_a_per_user_grant_is_not_reported_as_a_tenant_wide_one() -> None:
    client, _ = _client(
        grants=[
            _grant(RESOURCE_SP, "AllPrincipals", "Mail.Read Mail.ReadWrite"),
            _grant(RESOURCE_SP, "Principal", "Mail.Send"),
            _grant(OTHER_SP, "AllPrincipals", "Sites.Read.All"),
        ]
    )

    tenant_wide = _resource(client).get_delegated_permissions("app").execute_query().value

    assert sorted(tenant_wide) == ["Mail.Read", "Mail.ReadWrite"]


def test_every_consent_can_be_asked_for_explicitly() -> None:
    client, _ = _client(
        grants=[
            _grant(RESOURCE_SP, "AllPrincipals", "Mail.Read Mail.ReadWrite"),
            _grant(RESOURCE_SP, "Principal", "Mail.Send"),
        ]
    )

    everything = _resource(client).get_delegated_permissions("app", consent_type=None).execute_query().value

    assert sorted(everything) == ["Mail.Read", "Mail.ReadWrite", "Mail.Send"]


def test_revoking_a_scope_spares_the_grant_on_another_resource() -> None:
    elsewhere = _grant(OTHER_SP, "AllPrincipals", "Mail.Read")
    mine = _grant(RESOURCE_SP, "AllPrincipals", "Mail.Read")
    client, transport = _client(grants=[mine, elsewhere, _grant(RESOURCE_SP, "AllPrincipals", "Mail.Send")])

    _resource(client).revoke_delegated_permissions("app", "Mail.Read").execute_query()

    deletes = _requests(transport, HttpMethod.Delete)
    assert [request.url.rsplit("/", 1)[-1] for request in deletes] == [mine["id"]]


def test_every_grant_of_a_resource_is_read_not_just_the_first() -> None:
    client, _ = _client(
        grants=[
            _grant(RESOURCE_SP, "AllPrincipals", "Mail.Read"),
            _grant(RESOURCE_SP, "AllPrincipals", "Mail.ReadWrite Mail.Send"),
        ]
    )

    granted = _resource(client).get_delegated_permissions("app").execute_query().value

    assert sorted(granted) == ["Mail.Read", "Mail.ReadWrite", "Mail.Send"]
