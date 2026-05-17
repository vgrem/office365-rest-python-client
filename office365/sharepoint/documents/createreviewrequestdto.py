from office365.runtime.client_value import ClientValue
from typing import Optional


class CreateReviewRequestDTO(ClientValue):
    def __init__(self, document_uri: Optional[str] = None):
        self.document_uri = document_uri
