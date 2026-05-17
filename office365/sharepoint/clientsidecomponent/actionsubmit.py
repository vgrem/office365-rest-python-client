from office365.runtime.client_value import ClientValue
from typing import Optional


class ActionSubmit(ClientValue):
    def __init__(self, data: Optional[dict] = None):
        self.data = data
