from typing import Optional

from office365.runtime.client_value import ClientValue


class ScsEndpoint(ClientValue):
    def __init__(self, farm_label: Optional[str] = None, push_service_location: Optional[str] = None):
        self.FarmLabel = farm_label
        self.PushServiceLocation = push_service_location

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ScsEndpoint"
