from typing import Optional

from office365.runtime.client_value import ClientValue


class AdaptiveCardColumn(ClientValue):
    def __init__(self, width: Optional[str] = None):
        self.width = width
