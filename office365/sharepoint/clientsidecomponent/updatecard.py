from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.elementupdate import ElementUpdate


class UpdateCard(ClientValue):
    def __init__(
        self,
        card_updates: ClientValueCollection[ElementUpdate] = ClientValueCollection(ElementUpdate),
        type_: str = None,
    ):
        self.cardUpdates = card_updates
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.UpdateCard"
