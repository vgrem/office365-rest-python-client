from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class PivotItem(ClientValue):
    def __init__(self, audiences: StringCollection = StringCollection(), name: Optional[str] = None):
        self.audiences = audiences
        self.name = name
