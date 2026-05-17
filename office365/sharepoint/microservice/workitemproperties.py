from typing import Optional

from office365.runtime.client_value import ClientValue


class MicroServiceWorkItemProperties(ClientValue):
    def __init__(
        self,
        api_path: Optional[str] = None,
        custom_properties: Optional[dict] = None,
        http_headers: Optional[dict] = None,
        micro_service_name: Optional[str] = None,
        request_type: Optional[int] = None,
    ):
        self.ApiPath = api_path
        self.CustomProperties = custom_properties
        self.HttpHeaders = http_headers
        self.MicroServiceName = micro_service_name
        self.RequestType = request_type

    @property
    def entity_type_name(self):
        return "SP.MicroService.MicroServiceWorkItemProperties"
