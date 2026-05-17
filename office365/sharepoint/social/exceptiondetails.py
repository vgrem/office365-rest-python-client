from typing import Optional

from office365.runtime.client_value import ClientValue


class SocialExceptionDetails(ClientValue):
    def __init__(
        self,
        internal_error_code: Optional[int] = None,
        internal_message: Optional[str] = None,
        internal_stack_trace: Optional[str] = None,
        internal_type_name: Optional[str] = None,
        status: Optional[int] = None,
    ):
        self.InternalErrorCode = internal_error_code
        self.InternalMessage = internal_message
        self.InternalStackTrace = internal_stack_trace
        self.InternalTypeName = internal_type_name
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Social.SocialExceptionDetails"
