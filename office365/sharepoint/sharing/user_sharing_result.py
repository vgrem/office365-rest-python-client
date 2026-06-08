from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.role import Role


@dataclass
class UserSharingResult(ClientValue):
    """Specifies a sharing result for an individual user that method UpdateDocumentSharingInfo
    (section 3.2.5.187.2.1.1) returns.

    Args:
        AllowedRoles (list[int]): Specifies a set of roles that can be assigned to the user.
        CurrentRole (Role): Specifies the role that the user is currently assigned to.
        DisplayName (str): Gets the display name of the user.
        Email (str): Gets the user email.
        InvitationLink (str): Gets the invitation link.
        IsUserKnown (bool): Specifies whether the user is known to the server.
        If "true", the user is known to the server; if "false", user is unknown.
        Message (str): Specifies a message string that explains the reason when the Status  property is "false".
        Status (bool): Specifies whether the sharing update for the user was completed successfully.
        If "true", the sharing update completed successfully for the user; if "false", the sharing update failed
        for the user.
        User (str): Specifies the identifier of a user.
    """

    AllowedRoles: ClientValueCollection[Role] = field(default_factory=lambda: ClientValueCollection(Role))
    CurrentRole: Role | None = None
    DisplayName: str | None = None
    Email: str | None = None
    InvitationLink: str | None = None
    IsUserKnown: bool | None = None
    Message: str | None = None
    Status: bool | None = None
    User: str | None = None
    ExpirationDateTimeOnACE: datetime | None = None
    OtherMails: str | None = None

    @property
    def current_role_name(self):
        return str(self.CurrentRole)

    @property
    def entity_type_name(self):
        return "SP.Sharing"

    def __str__(self):
        return f"{self.User}: {self.current_role_name}"

    def __repr__(self):
        return f"{self.User}: {self.current_role_name}"
