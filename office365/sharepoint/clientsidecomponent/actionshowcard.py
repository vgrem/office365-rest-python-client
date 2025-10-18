from office365.runtime.client_value import ClientValue
from office365.sharepoint.clientsidecomponent.adaptivecard import AdaptiveCard


class ActionShowCard(ClientValue):

    def __init__(self, card: AdaptiveCard = AdaptiveCard()):
        self.card = card
