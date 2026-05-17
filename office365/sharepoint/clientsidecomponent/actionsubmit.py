from typing import Optional

from office365.runtime.client_value import ClientValue


class ActionSubmit(ClientValue):
    def __init__(self, data: Optional[dict] = None):
        self.data = data
