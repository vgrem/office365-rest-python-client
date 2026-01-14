from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.messagecardactionbutton import (
    MessageCardActionButton,
)
from office365.sharepoint.sitedesigns.messagecardinput import MessageCardInput


class PotentialAction(ClientValue):
    def __init__(
        self,
        actions: ClientValueCollection[MessageCardActionButton] = ClientValueCollection(MessageCardActionButton),
        inputs: ClientValueCollection[MessageCardInput] = ClientValueCollection(MessageCardInput),
        type_: str = None,
    ):
        self.actions = actions
        self.inputs = inputs
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.PotentialAction"
