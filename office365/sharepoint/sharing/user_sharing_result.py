from datetime import datetime
from typing import List

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.role import Role


class UserSharingResult(ClientValue):
    """Specifies a sharing result for an individual user that method UpdateDocumentSharingInfo
    (section 3.2.5.187.2.1.1) returns."""

    def __init__(
        self,
        allowed_roles: List[Role] = None,
        current_role: Role = None,
        display_name: str = None,
        email: str = None,
        invitation_link: str = None,
        is_user_known: bool = None,
        message: str = None,
        status: bool = None,
        user: str = None,
        expiration_date_time_on_ace: datetime = None,
        other_mails: str = None,
    ):
        """
        :param list[int] allowed_roles: Specifies a set of roles that can be assigned to the user.
        :param int current_role: Specifies the role that the user is currently assigned to.
        :param str display_name: Gets the display name of the user.
        :param str email: Gets the user email.
        :param str invitation_link: Gets the invitation link.
        :param bool is_user_known: Specifies whether the user is known to the server. If "true", the user is known to
            the server; if "false", user is unknown.
        :param str message: Specifies a message string that explains the reason when the Status  property is "false".
        :param bool status: Specifies whether the sharing update for the user was completed successfully. If "true",
            the sharing update completed successfully for the user; if "false", the sharing update failed for the user.
        :param str user: Specifies the identifier of a user.
        """
        super().__init__()
        self.AllowedRoles = ClientValueCollection(Role, allowed_roles)
        self.CurrentRole = current_role
        self.DisplayName = display_name
        self.Email = email
        self.InvitationLink = invitation_link
        self.IsUserKnown = is_user_known
        self.Message = message
        self.Status = status
        self.User = user
        self.ExpirationDateTimeOnACE = expiration_date_time_on_ace
        self.OtherMails = other_mails

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
