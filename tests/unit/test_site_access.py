"""Offline tests for ``Site.grant_access`` / ``Site.revoke_access`` and their app-aware twins.

Covers the request shape of the site-permission convenience wrappers: the
``POST /sites/{id}/permissions`` body for entity and object-ID identities, role
normalisation, the identity-matched deletes issued by ``revoke_access``, and the
application (client) ID / ``Application`` entity forms that resolve the service
principal internally.

The SharePoint REST side of the same two verbs lives here too: the
``Web.get_securable_object`` address builder and its ``grant_access`` /
``revoke_access`` wrappers.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.http.http_method import HttpMethod
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.permissions.roles.definitions.definition import RoleDefinition
from office365.sharepoint.principal.users.user import User
from tests import test_site_url
from tests._scripted_transport import RecordingTransport, RoutingTransport

SITE_ID = "contoso.sharepoint.com,site-guid,web-guid"
APP_ID = "11111111-1111-1111-1111-111111111111"
SP_OBJECT_ID = "22222222-2222-2222-2222-222222222222"


def _client(transport: RoutingTransport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def _site(client: GraphClient):
    return client.sites[SITE_ID]


def test_revoke_access_deletes_only_matching_permissions():
    payload = {
        "value": [
            {"id": "perm-1", "roles": ["write"], "grantedToIdentitiesV2": [{"application": {"id": APP_ID}}]},
            {"id": "perm-2", "roles": ["read"], "grantedToIdentitiesV2": [{"application": {"id": "someone-else"}}]},
            {"id": "perm-3", "roles": ["owner"], "grantedToV2": {"application": {"id": APP_ID}}},
        ]
    }
    transport = RoutingTransport([("permissions", payload)])
    client = _client(transport)

    _site(client).revoke_access(APP_ID).execute_query()

    deletes = [r.url.rsplit("/", 1)[-1] for r in transport.requests if r.method == HttpMethod.Delete]
    assert deletes == ["perm-1", "perm-3"]


def test_revoke_app_access_resolves_service_principal_and_deletes():
    payload = {
        "value": [
            {"id": "perm-1", "roles": ["write"], "grantedToIdentitiesV2": [{"application": {"id": SP_OBJECT_ID}}]},
            {"id": "perm-2", "roles": ["read"], "grantedToIdentitiesV2": [{"application": {"id": "someone-else"}}]},
        ]
    }
    transport = RoutingTransport(
        [
            ("servicePrincipals", {"id": SP_OBJECT_ID, "displayName": "Contoso App"}),
            ("permissions", payload),
        ]
    )
    client = _client(transport)

    _site(client).revoke_app_access(APP_ID).execute_query()

    deletes = [r.url.rsplit("/", 1)[-1] for r in transport.requests if r.method == HttpMethod.Delete]
    assert deletes == ["perm-1"]


# --- The SharePoint REST side: get_securable_object and its wrappers ----------


PRINCIPAL_ID = 6
ROLE_DEF_ID = 1073741827


def _ctx() -> ClientContext:
    return ClientContext(test_site_url)


# --- Web.get_securable_object -------------------------------------------------


def test_scope_is_case_insensitive():
    ctx = _ctx()

    assert ctx.web.get_securable_object("WEB") is ctx.web
    assert isinstance(ctx.web.get_securable_object("Folder", url="/sites/x/f"), ListItem)


# --- SecurableObject.grant_access / revoke_access -----------------------------


def _loaded_principal(ctx) -> User:
    principal = User(ctx)
    principal.set_property("Id", PRINCIPAL_ID)
    return principal


def _loaded_role(ctx) -> RoleDefinition:
    role = RoleDefinition(ctx)
    role.set_property("Id", ROLE_DEF_ID)
    return role


def test_grant_access_is_deferred():
    ctx = _ctx()
    ctx.pending_request().beforeExecute.clear()
    transport = RecordingTransport([])
    ctx.pending_request().transport = transport
    target = ctx.web.get_securable_object("web")

    target.grant_access(_loaded_principal(ctx), _loaded_role(ctx))

    assert transport.calls == 0
    assert transport.requests == []
