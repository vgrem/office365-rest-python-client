from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PermissionRequirement:
    """Declares the permissions required to call an API method.

    Fields map directly to the official Microsoft Graph docs tables
    (Delegated / Application columns, plus optional Entra ID roles).

    Stamped as ``method.__required_permissions__`` by :func:`require_permission`.
    """

    delegated: list[str] = field(default_factory=list)
    application: list[str] = field(default_factory=list)
    directory_roles: list[str] = field(default_factory=list)
    notes: str = ""


def require_permission(
    delegated: list[str] | None = None,
    application: list[str] | None = None,
    directory_roles: list[str] | None = None,
    notes: str = "",
):
    """Annotate a method with the permissions it requires.

    This is a **metadata-only** decorator — it stamps permission information
    on the function and enriches its docstring so that ``help(method)``
    displays the required permissions.  There is **zero runtime overhead**:
    no network calls, no authentication, no type checking.

    The ``delegated`` and ``application`` parameters map directly to the
    columns in the official Microsoft Graph REST API documentation.

    View the declared permissions with :func:`help`::

        from office365.onedrive.drives.collection import DriveCollection

        help(DriveCollection.get)
    """
    req = PermissionRequirement(
        delegated=delegated or [],
        application=application or [],
        directory_roles=directory_roles or [],
        notes=notes,
    )

    def decorator(func):
        func.__required_permissions__ = req

        lines: list[str] = []
        if req.delegated:
            lines.append(f"      Delegated: {', '.join(req.delegated)}")
        if req.application:
            lines.append(f"      Application: {', '.join(req.application)}")
        if req.directory_roles:
            lines.append(f"      Directory roles: {', '.join(req.directory_roles)}")
        if req.notes:
            lines.append(f"      Notes: {req.notes}")

        if lines:
            extra = "\n    Requires permissions:\n" + "\n".join(lines)
            func.__doc__ = (func.__doc__ or "") + extra

        return func

    return decorator
