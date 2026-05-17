from office365.runtime.client_value import ClientValue
from typing import Optional


class AdaptiveCardColumn(ClientValue):
    def __init__(self, width: Optional[str] = None):
        self.width = width
