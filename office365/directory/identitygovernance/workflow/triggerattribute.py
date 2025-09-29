from office365.runtime.client_value import ClientValue


class TriggerAttribute(ClientValue):

    def __init__(self, name: str = None):
        self.name = name
