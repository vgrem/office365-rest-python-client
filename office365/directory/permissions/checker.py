from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from office365.directory.permissions.guard import ResourcePermissions, get_permissions
from office365.directory.permissions.require_permission import PermissionRequirement
from office365.directory.permissions.resource_name import ResourceName
from office365.graph_client import GraphClient


@dataclass
class PermissionReport:
    """Result of verifying declared permissions against actual Entra ID grants.

    This is a **diagnostic-only** dataclass — it never raises, never blocks,
    and never modifies state.  Use it after a 401 to understand what went wrong.

    Fields:
        method: Name of the annotated method that was checked
        required: The ``PermissionRequirement`` stamped by ``@require_permission``
        perms: The ``ResourcePermissions`` fetched from the service principal
        granted_roles: Entra ID directory roles the signed-in user has

    Properties ``granted_delegated``, ``granted_application``,
    ``missing_delegated``, ``missing_application``, and ``has_all`` are
    computed from ``required`` vs ``perms``.
    """

    perms: ResourcePermissions
    _method: Any = field(repr=False, default=None)
    _client: Any = field(repr=False, default=None)

    @property
    def method(self) -> str:
        name = self._method.__qualname__ if self._method else "(unknown)"
        if self._method and not getattr(self._method, "__required_permissions__", None):
            name += " (no @require_permission)"
        return name

    @property
    def required(self) -> PermissionRequirement:
        return getattr(self._method, "__required_permissions__", None) or PermissionRequirement()

    @property
    def granted_delegated(self) -> list[str]:
        return [s for s in self.required.delegated if s in self.perms.delegated]

    @property
    def granted_application(self) -> list[str]:
        return [s for s in self.required.application if s in self.perms.application]

    @property
    def missing_delegated(self) -> list[str]:
        return [s for s in self.required.delegated if s not in self.perms.delegated]

    @property
    def missing_application(self) -> list[str]:
        return [s for s in self.required.application if s not in self.perms.application]

    @property
    def granted_roles(self) -> list[str]:
        req = self.required
        if not req.directory_roles or not self._client:
            return []
        from office365.directory.permissions.guard import has_role

        return [r for r in req.directory_roles if has_role(self._client, r)]

    @property
    def has_all(self) -> bool:
        return not self.missing_delegated and not self.missing_application

    def __str__(self) -> str:
        return json.dumps(
            {
                "method": self.method,
                "required": vars(self.required),
                "granted": {"delegated": self.granted_delegated, "application": self.granted_application},
                "missing": {"delegated": self.missing_delegated, "application": self.missing_application},
                "has_all": self.has_all,
            },
            indent=2,
        )


def verify_permissions(
    client: GraphClient,
    method,
    client_id: str | None = None,
) -> PermissionReport:
    if client_id is None:
        client_id = getattr(client, "_client_id", None)
        if client_id is None:
            raise ValueError(
                "client_id is required. Pass it explicitly or call "
                "with_client_secret / with_certificate on the GraphClient first."
            )
    """Check whether the permissions declared on a method are actually granted.

    Reads the ``@require_permission`` metadata from the method and compares
    each declared scope against the application's Entra ID service principal
    via the Microsoft Graph ``servicePrincipals`` API.

    This is a **diagnostic-only** function — it never raises, never blocks,
    and never makes any changes.  Use it after encountering a 401 to identify
    which scopes are missing.

    Args:
        client: An authenticated ``GraphClient`` — only Microsoft Graph
            exposes the ``servicePrincipals`` endpoint needed to query
            granted permissions.
        method: The annotated function, method, or property getter to check.
        client_id: Application client ID.  If omitted, the value stored by
            ``with_client_secret`` / ``with_certificate`` is used.

    Returns:
        A :class:`PermissionReport` describing which scopes are present
        and which are missing.
    """

    perms = get_permissions(client, client_id, ResourceName.Graph)

    return PermissionReport(_method=method, perms=perms, _client=client)
