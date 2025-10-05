from office365.runtime.client_value import ClientValue


class SocialExceptionDetails(ClientValue):

    def __init__(
        self,
        internal_error_code: int = None,
        internal_message: str = None,
        internal_stack_trace: str = None,
        internal_type_name: str = None,
        status: int = None,
    ):
        self.InternalErrorCode = internal_error_code
        self.InternalMessage = internal_message
        self.InternalStackTrace = internal_stack_trace
        self.InternalTypeName = internal_type_name
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Social.SocialExceptionDetails"
