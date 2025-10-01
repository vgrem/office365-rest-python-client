from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class Error(ClientValue):

    def __init__(self, details: StringCollection = StringCollection()):
        self.Details = details
