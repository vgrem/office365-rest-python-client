"""Reusable permission and role check functions for Microsoft Graph.

Usage:
    from office365.directory.permissions.guard import has_delegated_permission, has_app_permission, has_role

    if has_delegated_permission(client, "Mail.Read", client_id):
        send_mail()

    if has_app_permission(client, "Application.Read.All", client_id):
        list_apps()

    if has_role(client, "Global Administrator"):
        do_admin_stuff()
"""

from __future__ import annotations

from functools import lru_cache

from office365.directory.applications.roles.collection import AppRoleCollection
from office365.directory.rolemanagement.role import DirectoryRole
from office365.entity_collection import EntityCollection
from office365.graph_client import GraphClient
from office365.runtime.types.collections import StringCollection


@lru_cache(maxsize=1)
def _cached_app_permissions(client: GraphClient, client_id: str) -> AppRoleCollection:
    """Get and cache application permissions for a client."""
    resource = client.service_principals.get_by_name("Microsoft Graph")
    result = resource.get_application_permissions(client_id).execute_query()
    return result.value  # type: ignore[return-value]


@lru_cache(maxsize=1)
def _cached_delegated_permissions(client: GraphClient, client_id: str) -> StringCollection:
    """Get and cache delegated permissions for a client."""
    resource = client.service_principals.get_by_name("Microsoft Graph")
    result = resource.get_delegated_permissions(client_id).execute_query()
    return result.value  # type: ignore[return-value]


@lru_cache(maxsize=1)
def _cached_directory_roles(client: GraphClient) -> EntityCollection[DirectoryRole]:
    """Get and cache the signed-in user's directory roles."""
    result = client.me.get_directory_roles().execute_query()
    return result  # type: ignore[return-value]


def has_delegated_permission(client: GraphClient, scope: str, client_id: str) -> bool:
    """True if the app has the delegated permission (OAuth scope) assigned."""
    return scope in _cached_delegated_permissions(client, client_id)


def has_app_permission(client: GraphClient, scope: str, client_id: str) -> bool:
    """True if the app has the application permission (app role) assigned."""
    return any(role.value == scope for role in _cached_app_permissions(client, client_id))


def has_role(client: GraphClient, role_name: str) -> bool:
    """True if the signed-in user has the directory role."""
    return any(role.display_name == role_name for role in _cached_directory_roles(client))
