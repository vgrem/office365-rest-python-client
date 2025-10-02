from office365.runtime.client_value import ClientValue


class PortalHealthStatusDetails(ClientValue):

    def __init__(
        self,
        error_reason: str = None,
        help_link: str = None,
        portal_health_error_code: int = None,
        status: int = None,
    ):
        self.ErrorReason = error_reason
        self.HelpLink = help_link
        self.PortalHealthErrorCode = portal_health_error_code
        self.Status = status
