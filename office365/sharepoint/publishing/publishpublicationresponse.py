from office365.runtime.client_value import ClientValue


class PublishPublicationResponse(ClientValue):

    def __init__(self, error_code: int = None, message: str = None, status: bool = None):
        self.ErrorCode = error_code
        self.Message = message
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishPublicationResponse"
