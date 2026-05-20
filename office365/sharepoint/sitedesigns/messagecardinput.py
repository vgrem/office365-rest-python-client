from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.choice import Choice


@dataclass
class MessageCardInput(ClientValue):
    choices: ClientValueCollection[Choice] = field(default_factory=lambda: ClientValueCollection(Choice))
    id: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCardInput"
