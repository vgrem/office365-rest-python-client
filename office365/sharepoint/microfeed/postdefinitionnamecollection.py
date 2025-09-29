from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MicrofeedPostDefinitionNameCollection(ClientValue):

    def __init__(self, items: StringCollection = StringCollection()):
        self.Items = items
