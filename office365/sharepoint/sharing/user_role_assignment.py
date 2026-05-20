from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.role import Role


@dataclass
class UserRoleAssignment(ClientValue):
    """Specifies a user and a role that is associated with the user."""

    Role: Role | None = None
    UserId: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.UserRoleAssignment"
