from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.header import Header


@dataclass
class MessageCardActionButton(ClientValue):
    body: Optional[str] = None
    bodyContentType: Optional[str] = None
    headers: ClientValueCollection[Header] = field(default_factory=lambda: ClientValueCollection(Header))
    name: Optional[str] = None
    target: Optional[str] = None
    type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCardActionButton"
