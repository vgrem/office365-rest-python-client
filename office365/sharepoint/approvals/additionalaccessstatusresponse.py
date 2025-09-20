from office365.runtime.client_value import ClientValue


class AdditionalAccessStatusResponse(ClientValue):

    def __init__(
        self,
        additional_access_request_status: int = None,
        error_message: str = None,
        role_value: int = None,
        status_code: int = None,
    ):
        self.additional_access_request_status = additional_access_request_status
        self.error_message = error_message
        self.role_value = role_value
        self.status_code = status_code
