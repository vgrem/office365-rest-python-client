from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.role import Role


@dataclass
class UserRoleAssignment(ClientValue):
    """
    Specifies a user and a role that is associated with the user.

    Fields:
        Role: Specifies a Role (section 3.2.5.188) that is assigned to a user.
        UserId: Specifies the identifier of a user, which can be in the format of an email address or a login
            identifier.
    """

    Role: Role | None = None
    UserId: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.UserRoleAssignment"
