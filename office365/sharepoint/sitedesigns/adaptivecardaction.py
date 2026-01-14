from office365.runtime.client_value import ClientValue


class AdaptiveCardAction(ClientValue):
    def __init__(self, is_primary: bool = None, title: str = None):
        self.is_primary = is_primary
        self.title = title
