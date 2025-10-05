from office365.runtime.client_value import ClientValue


class ToolDetails(ClientValue):

    def __init__(self, name: str = None, version: str = None):
        self.Name = name
        self.Version = version
