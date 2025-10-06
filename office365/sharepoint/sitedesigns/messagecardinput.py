from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.choice import Choice


class MessageCardInput(ClientValue):

    def __init__(
        self,
        choices: ClientValueCollection[Choice] = ClientValueCollection(Choice),
        id_: str = None,
        type_: str = None,
        value: str = None,
    ):
        self.choices = choices
        self.id = id_
        self.type = type_
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCardInput"
