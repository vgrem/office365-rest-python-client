from office365.runtime.client_value import ClientValue


class ListDataSource(ClientValue):
    def __init__(self, properties: dict = None):
        self.Properties = properties

    "Stores the parameters required for a list to communicate with its external data source."
