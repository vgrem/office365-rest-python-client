from office365.runtime.client_value import ClientValue


class ScsEndpoint(ClientValue):

    def __init__(self, farm_label: str = None, push_service_location: str = None):
        self.FarmLabel = farm_label
        self.PushServiceLocation = push_service_location

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ScsEndpoint"
