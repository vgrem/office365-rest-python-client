from office365.runtime.client_value import ClientValue
from typing import Optional


class OwnedByMeParams(ClientValue):
    def __init__(self, top: Optional[int] = None):
        self.Top = top
