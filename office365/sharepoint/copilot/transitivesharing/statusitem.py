from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CopilotTransitiveSharingStatusItem(ClientValue):
    ListId: Optional[str] = None
    SiteId: Optional[str] = None
    Status: Optional[int] = None
    UniqueId: Optional[str] = None
    Url: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotTransitiveSharingStatusItem"
