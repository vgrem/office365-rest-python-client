from office365.runtime.client_value import ClientValue
from typing import Optional


class AdaptiveCardAction(ClientValue):
    def __init__(self, is_primary: Optional[bool] = None, title: Optional[str] = None):
        self.is_primary = is_primary
        self.title = title
