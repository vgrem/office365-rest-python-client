from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.adaptivecardaction import AdaptiveCardAction
from typing import Optional


class ActionSet(ClientValue):
    def __init__(
        self,
        actions: ClientValueCollection[AdaptiveCardAction] = ClientValueCollection(AdaptiveCardAction),
        horizontal_alignment: Optional[str] = None,
    ):
        self.actions = actions
        self.horizontal_alignment = horizontal_alignment
