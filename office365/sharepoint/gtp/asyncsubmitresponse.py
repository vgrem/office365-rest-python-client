from typing import Optional

from office365.runtime.client_value import ClientValue


class GptAsyncSubmitResponse(ClientValue):
    def __init__(
        self, error_message: Optional[str] = None, failure_reason: Optional[str] = None, status: Optional[str] = None
    ):
        self.ErrorMessage = error_message
        self.FailureReason = failure_reason
        self.Status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptAsyncSubmitResponse"
