from typing import Optional

from office365.runtime.client_value import ClientValue


class PortalHealthStatusDetails(ClientValue):
    def __init__(
        self,
        error_reason: Optional[str] = None,
        help_link: Optional[str] = None,
        portal_health_error_code: Optional[int] = None,
        status: Optional[int] = None,
    ):
        self.ErrorReason = error_reason
        self.HelpLink = help_link
        self.PortalHealthErrorCode = portal_health_error_code
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatusDetails"
