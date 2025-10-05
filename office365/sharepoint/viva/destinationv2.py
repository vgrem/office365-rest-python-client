from office365.runtime.client_value import ClientValue


class VivaEngageDestinationV2(ClientValue):

    def __init__(self, destination_name: str = None, destination_type: int = None):
        self.DestinationName = destination_name
        self.DestinationType = destination_type

    @property
    def entity_type_name(self):
        return "SP.Publishing.VivaEngageDestinationV2"
