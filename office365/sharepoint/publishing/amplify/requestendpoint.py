from office365.runtime.client_value import ClientValue


class AmplifyRequestEndpoint(ClientValue):
    def __init__(self, data: str = None, endpoint_type: int = None):
        self.Data = data
        self.EndpointType = endpoint_type

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyRequestEndpoint"
