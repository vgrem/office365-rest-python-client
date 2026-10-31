from __future__ import annotations

import json
from dataclasses import dataclass, field

from office365.directory.permissions.guard import (
    ResourcePermissions,
    _cached_app_permissions,
    _cached_delegated_permissions,
)
from office365.graph_client import GraphClient
from office365.permissions import PermissionRequirement, declared


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

    method: str
    required: PermissionRequirement
    perms: ResourcePermissions
    granted_roles: list[str] = field(default_factory=list)

    @property
    def resource(self) -> str:
        """The API the checked permissions belong to, as the declaration named it."""
        return self.perms.resource

    @property
    def granted_delegated(self) -> list[str]:
        return [s for s in self.required.delegated if s in self.perms.delegated]

    @property
    def granted_application(self) -> list[str]:
        return [s for s in self.required.application if s in self.perms.application]

    def __str__(self) -> str:
        return json.dumps(
            {
                "method": self.method,
                "resource": self.resource,
                "delegated": ", ".join(self.granted_delegated),
                "application": ", ".join(self.granted_application),
            }
        )


def verify_permissions(
    client: GraphClient,
    method,
    client_id: str | None = None,
) -> PermissionReport:
    """Check whether the permissions declared on a method are actually granted.

    Reads the ``@require_permission`` metadata from the method and compares
    each declared scope against the grants held by the service principal of
    the resource the declaration names - Microsoft Graph by default, or e.g.
    ``Office 365 SharePoint Online`` for a declaration on
    :mod:`office365.sharepoint`. The names are only comparable within that
    resource, which is why the declaration carries it.

    This is a **diagnostic-only** function: it never raises on a missing grant
    and never makes any changes. Use it after encountering a 401 to identify
    which scopes are missing. A method that declares nothing is a different
    mistake - it raises, through :func:`~office365.permissions.declared`.

    Args:
        client: An authenticated ``GraphClient`` - only Microsoft Graph
            exposes the ``servicePrincipals`` endpoint needed to query
            granted permissions, whatever resource they were granted on.
        method: The annotated function, method, or property getter to check.
        client_id: Application client ID.  If omitted, the value stored by
            ``with_client_secret`` / ``with_certificate`` is used.

    Returns:
        A :class:`PermissionReport` describing which scopes are present
        and which are missing.
    """

    if client_id is None:
        client_id = getattr(client, "_client_id", None)
        if client_id is None:
            raise ValueError(
                "client_id is required. Pass it explicitly or call "
                "with_client_secret / with_certificate on the GraphClient first."
            )

    req: PermissionRequirement = declared(method)
    resource = req.resource
    app_roles = _cached_app_permissions(client, client_id, resource)
    delegated_scopes = _cached_delegated_permissions(client, client_id, resource)
    perms = ResourcePermissions(
        resource=resource,
        application=[r.value for r in app_roles if r.value is not None],
        delegated=list(delegated_scopes),
    )

    granted_roles: list[str] = []
    if req.directory_roles:
        from office365.directory.permissions.guard import has_role

        granted_roles = [r for r in req.directory_roles if has_role(client, r)]

    return PermissionReport(
        method=method.__qualname__,
        required=req,
        perms=perms,
        granted_roles=granted_roles,
    )
