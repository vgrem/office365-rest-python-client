"""Reusable permission and role check functions for Microsoft Graph and other Entra ID resources.

Every check names the *resource* it asks about, because a permission name is only a grant on the
API that defines it: ``Sites.ReadWrite.All`` on Graph and ``Sites.ReadWrite.All`` on SharePoint
are two grants, and ``Mail.Send`` is an application permission on Graph but a delegated one on
Exchange Online. The default is Microsoft Graph, and the name is resolved to that resource's
service principal rather than assumed.

Usage:
    from office365.directory.permissions.guard import has_delegated_permission, has_role
    from office365.permissions import ResourceName

    if has_delegated_permission(client, "Mail.Read", client_id):
        read_mail()

    if has_delegated_permission(client, "Sites.Read.All", client_id, ResourceName.SharePoint):
        download_file()

    if has_application_permission(client, "Application.Read.All", client_id):
        list_apps()

    if has_role(client, "Global Administrator"):
        do_admin_stuff()
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from office365.directory.applications.roles.collection import AppRoleCollection
from office365.directory.rolemanagement.roles.role import DirectoryRole
from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from office365.entity_collection import EntityCollection
from office365.graph_client import GraphClient
from office365.permissions import ResourceName
from office365.runtime.types.collections import StringCollection


@dataclass
class ResourcePermissions:
    """All granted permissions for a given Entra ID resource."""

    resource: str
    application: list[str] = field(default_factory=list)
    delegated: list[str] = field(default_factory=list)


def _resource_principal(client: GraphClient, resource: str) -> ServicePrincipal:
    """The service principal that owns ``resource``'s permission definitions and grants."""
    return client.service_principals.find_by_name(resource, required=True)


@lru_cache(maxsize=None)
def _cached_app_permissions(
    client: GraphClient, client_id: str, resource: str = ResourceName.Graph
) -> AppRoleCollection:
    """Get and cache the application permissions granted to ``client_id`` on ``resource``."""
    return _resource_principal(client, resource).get_application_permissions(client_id).execute_query().value


@lru_cache(maxsize=None)
def _cached_delegated_permissions(
    client: GraphClient, client_id: str, resource: str = ResourceName.Graph
) -> StringCollection:
    """Get and cache the delegated permissions granted to ``client_id`` on ``resource``."""
    return _resource_principal(client, resource).get_delegated_permissions(client_id).execute_query().value


@lru_cache(maxsize=1)
def _cached_directory_roles(client: GraphClient) -> EntityCollection[DirectoryRole]:
    """Get and cache the signed-in user's directory roles."""
    result = client.me.get_directory_roles().execute_query()
    return result


def has_delegated_permission(
    client: GraphClient, scope: str, client_id: str, resource: str = ResourceName.Graph
) -> bool:
    """True if the app has the delegated permission (OAuth scope) assigned on the resource."""
    return scope in _cached_delegated_permissions(client, client_id, resource)


def has_application_permission(
    client: GraphClient, app_role: str, client_id: str, resource: str = ResourceName.Graph
) -> bool:
    """True if the app has the application permission (app role) assigned on the resource."""
    return app_role in {role.value for role in _cached_app_permissions(client, client_id, resource)}


def has_role(client: GraphClient, *role_names: str) -> bool:
    """True if the signed-in user has at least one of the specified directory roles."""
    granted = {r.display_name for r in _cached_directory_roles(client)}
    return any(role in granted for role in role_names)
