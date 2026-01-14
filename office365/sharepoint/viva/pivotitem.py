from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class PivotItem(ClientValue):
    def __init__(self, audiences: StringCollection = StringCollection(), name: str = None):
        self.audiences = audiences
        self.name = name
