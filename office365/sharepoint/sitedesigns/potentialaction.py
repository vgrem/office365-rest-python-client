from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.sitedesigns.messagecardactionbutton import (
    MessageCardActionButton,
)
from office365.sharepoint.sitedesigns.messagecardinput import MessageCardInput


@value
class PotentialAction(ClientValue):
    actions: ClientValueCollection[MessageCardActionButton] = field(
        default_factory=lambda: ClientValueCollection(MessageCardActionButton)
    )
    inputs: ClientValueCollection[MessageCardInput] = field(
        default_factory=lambda: ClientValueCollection(MessageCardInput)
    )
    type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.PotentialAction"
