from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SharedWithMeDocumentUser(ClientValue):
    """Represents a user of a document that is shared with the current user."""

    Id: Optional[str] = None
    LoginName: Optional[str] = None
    SipAddress: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.UserProfiles.SharedWithMeDocumentUser"
