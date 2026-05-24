from __future__ import annotations

import json
from dataclasses import dataclass, field

from office365.directory.permissions.guard import get_permissions
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
        missing_delegated: Declared delegated scopes NOT found in the service principal
        missing_application: Declared application scopes NOT found
        granted_delegated: Delegated scopes the app actually has
        granted_application: Application scopes the app actually has
        granted_roles: Entra ID directory roles the signed-in user has
    """

    method: str
    required: PermissionRequirement
    missing_delegated: list[str] = field(default_factory=list)
    missing_application: list[str] = field(default_factory=list)
    granted_delegated: list[str] = field(default_factory=list)
    granted_application: list[str] = field(default_factory=list)
    granted_roles: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return json.dumps({
            "method": self.method,
            "required": {
                "delegated": self.required.delegated,
                "application": self.required.application,
            },
            "granted": {
                "delegated": self.granted_delegated,
                "application": self.granted_application,
            },
            "missing": {
                "delegated": self.missing_delegated,
                "application": self.missing_application,
            },
            "has_all": self.has_all,
        }, indent=2)

    @property
    def has_all(self) -> bool:
        """``True`` when no scopes are missing (directory roles are NOT checked)."""
        return not self.missing_delegated and not self.missing_application


def verify_permissions(
    client: GraphClient,
    method,
    client_id: str | None = None,
) -> PermissionReport:
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

    req: PermissionRequirement | None = getattr(method, "__required_permissions__", None)
    if req is None:
        return PermissionReport(
            method=getattr(method, "__name__", str(method)),
            required=PermissionRequirement(),
            missing_delegated=["(no @require_permission annotation found)"],
        )

    if client_id is None:
        client_id = getattr(client, "_client_id", None)
        if client_id is None:
            return PermissionReport(
                method=getattr(method, "__name__", str(method)),
                required=req,
                missing_delegated=["(client_id unknown)"],
                missing_application=["(client_id unknown)"],
            )

    perms = get_permissions(client, client_id, ResourceName.Graph)

    missing_delegated: list[str] = []
    missing_application: list[str] = []
    granted_delegated: list[str] = []
    granted_application: list[str] = []

    for scope in req.delegated:
        if scope in perms.delegated:
            granted_delegated.append(scope)
        else:
            missing_delegated.append(scope)

    for scope in req.application:
        if scope in perms.application:
            granted_application.append(scope)
        else:
            missing_application.append(scope)

    granted_roles: list[str] = []
    if req.directory_roles:
        from office365.directory.permissions.guard import has_role
        for role in req.directory_roles:
            if has_role(client, role):
                granted_roles.append(role)

    return PermissionReport(
        method=getattr(method, "__name__", str(method)),
        required=req,
        missing_delegated=missing_delegated,
        missing_application=missing_application,
        granted_delegated=granted_delegated,
        granted_application=granted_application,
        granted_roles=granted_roles,
    )
