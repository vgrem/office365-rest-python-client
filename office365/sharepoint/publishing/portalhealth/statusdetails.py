from typing import Optional

from office365.runtime.client_value import ClientValue


class PortalHealthStatusDetails(ClientValue):
    ErrorReason: Optional[str] = None
    HelpLink: Optional[str] = None
    PortalHealthErrorCode: Optional[int] = None
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatusDetails"
