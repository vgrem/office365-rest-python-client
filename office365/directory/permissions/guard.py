"""Reusable permission and role check functions for Microsoft Graph and other Entra ID resources.

Usage:
    from office365.directory.permissions.guard import has_delegated_permission, has_app_permission, has_role
    from office365.directory.permissions.resource_name import ResourceName

    if has_delegated_permission(client, "Mail.Read", client_id):
        send_mail()

    if has_app_permission(client, "Application.Read.All", client_id):
        list_apps()

    if has_app_permission(client, "Sites.Read.All", client_id, ResourceName.SharePoint):
        download_file()

    if has_role(client, "Global Administrator"):
        do_admin_stuff()
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from office365.directory.applications.roles.collection import AppRoleCollection
from office365.directory.permissions.resource_name import ResourceName
from office365.directory.rolemanagement.role import DirectoryRole
from office365.entity_collection import EntityCollection
from office365.graph_client import GraphClient
from office365.runtime.types.collections import StringCollection


@dataclass
class ResourcePermissions:
    """All granted permissions for a given Entra ID resource."""

    resource: str
    application: list[str] = field(default_factory=list)
    delegated: list[str] = field(default_factory=list)


@lru_cache(maxsize=None)
def _cached_app_permissions(
    client: GraphClient, client_id: str, resource: str = ResourceName.Graph
) -> AppRoleCollection:
    """Get and cache application permissions for a client on a given resource."""
    resource_name = resource.value if isinstance(resource, ResourceName) else resource
    sp = client.service_principals.get_by_name(resource_name)
    result = sp.get_application_permissions(client_id).execute_query()
    return result.value  # type: ignore[return-value]


@lru_cache(maxsize=None)
def _cached_delegated_permissions(
    client: GraphClient, client_id: str, resource: str = ResourceName.Graph
) -> StringCollection:
    """Get and cache delegated permissions for a client on a given resource."""
    resource_name = resource.value if isinstance(resource, ResourceName) else resource
    sp = client.service_principals.get_by_name(resource_name)
    result = sp.get_delegated_permissions(client_id).execute_query()
    return result.value  # type: ignore[return-value]


@lru_cache(maxsize=1)
def _cached_directory_roles(client: GraphClient) -> EntityCollection[DirectoryRole]:
    """Get and cache the signed-in user's directory roles."""
    result = client.me.get_directory_roles().execute_query()
    return result  # type: ignore[return-value]


def has_delegated_permission(
    client: GraphClient, scope: str, client_id: str, resource: str = ResourceName.Graph
) -> bool:
    """True if the app has the delegated permission (OAuth scope) assigned on the resource."""
    return scope in _cached_delegated_permissions(client, client_id, resource)


def has_app_permission(client: GraphClient, scope: str, client_id: str, resource: str = ResourceName.Graph) -> bool:
    """True if the app has the application permission (app role) assigned on the resource."""
    return any(role.value == scope for role in _cached_app_permissions(client, client_id, resource))


def get_permissions(client: GraphClient, client_id: str, resource: str = ResourceName.Graph) -> ResourcePermissions:
    """Get all granted permissions (app roles + delegated scopes) for a resource.

    Args:
        client: Authenticated GraphClient
        client_id: Application (client) ID
        resource: Service principal name from ResourceName enum

    Returns:
        ResourcePermissions with application and delegated permission lists
    """
    app_roles = _cached_app_permissions(client, client_id, resource)
    delegated_scopes = _cached_delegated_permissions(client, client_id, resource)
    return ResourcePermissions(
        resource=resource,
        application=[r.value for r in app_roles if r.value is not None],
        delegated=list(delegated_scopes),
    )


def has_role(client: GraphClient, role_name: str) -> bool:
    """True if the signed-in user has the directory role."""
    return any(role.display_name == role_name for role in _cached_directory_roles(client))
