from typing import Optional

from office365.runtime.client_value import ClientValue


class OwnedByMeParams(ClientValue):
    def __init__(self, top: Optional[int] = None):
        self.Top = top
