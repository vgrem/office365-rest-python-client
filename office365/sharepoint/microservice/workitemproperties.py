from office365.runtime.client_value import ClientValue


class MicroServiceWorkItemProperties(ClientValue):

    def __init__(
        self,
        api_path: str = None,
        custom_properties: dict = None,
        http_headers: dict = None,
        micro_service_name: str = None,
        request_type: int = None,
    ):
        self.ApiPath = api_path
        self.CustomProperties = custom_properties
        self.HttpHeaders = http_headers
        self.MicroServiceName = micro_service_name
        self.RequestType = request_type

    @property
    def entity_type_name(self):
        return "SP.MicroService.MicroServiceWorkItemProperties"
