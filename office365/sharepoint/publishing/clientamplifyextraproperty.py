from office365.runtime.client_value import ClientValue


class ClientAmplifyExtraProperty(ClientValue):

    def __init__(self, name: str = None, value: str = None):
        self.name = name
        self.value = value
