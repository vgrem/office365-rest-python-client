from typing import Optional

from office365.runtime.client_value import ClientValue


class MicroServiceWorkItemProperties(ClientValue):
    ApiPath: Optional[str] = None
    CustomProperties: Optional[dict] = None
    HttpHeaders: Optional[dict] = None
    MicroServiceName: Optional[str] = None
    RequestType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.MicroService.MicroServiceWorkItemProperties"
