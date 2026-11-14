from __future__ import annotations

from office365.directory.permissions.identity import Identity


class UserIdentity(Identity):
    """
    In the context of an Azure AD audit log, this represents the user information that initiated or
    was affected by an audit activity.
    """

    displayName: str | None = None
    ipAddress: str | None = None
    userPrincipalName: str | None = None

    def __str__(self) -> str:
        """Best-effort human-readable label (name, UPN or IP)."""
        return self.displayName or self.userPrincipalName or self.ipAddress or ""

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserIdentity"
