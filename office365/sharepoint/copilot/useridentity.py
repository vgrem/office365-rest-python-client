from typing import Optional

from office365.runtime.client_value import ClientValue


class UserIdentity(ClientValue):
    def __init__(
        self, display_name: Optional[str] = None, email: Optional[str] = None, login_name: Optional[str] = None
    ):
        self.DisplayName = display_name
        self.Email = email
        self.LoginName = login_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.UserIdentity"
