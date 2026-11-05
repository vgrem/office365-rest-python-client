from typing import Optional

from office365.runtime.client_value import ClientValue


class UserIdentity(ClientValue):
    DisplayName: Optional[str] = None
    Email: Optional[str] = None
    LoginName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.UserIdentity"
