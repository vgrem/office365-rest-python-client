from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class VivaSiteRequestInfo(ClientValue):
    """Viva site request information.

    Fields:
        is_already_added (bool):
        site_url (str):
    """

    IsAlreadyAdded: Optional[bool] = None
    SiteUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.VivaSiteRequestInfo"
