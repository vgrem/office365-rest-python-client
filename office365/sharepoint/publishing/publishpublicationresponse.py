from typing import Optional

from office365.runtime.client_value import ClientValue


class PublishPublicationResponse(ClientValue):
    def __init__(self, error_code: Optional[int] = None, message: Optional[str] = None, status: Optional[bool] = None):
        self.ErrorCode = error_code
        self.Message = message
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishPublicationResponse"
