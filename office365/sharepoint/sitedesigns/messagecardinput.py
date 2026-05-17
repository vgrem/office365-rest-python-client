from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.choice import Choice
from typing import Optional


class MessageCardInput(ClientValue):
    def __init__(
        self,
        choices: ClientValueCollection[Choice] = ClientValueCollection(Choice),
        id_: Optional[str] = None,
        type_: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.choices = choices
        self.id = id_
        self.type = type_
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCardInput"
