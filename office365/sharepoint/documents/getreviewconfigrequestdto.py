from typing import Optional

from office365.runtime.client_value import ClientValue


class GetReviewConfigRequestDTO(ClientValue):
    def __init__(self, document_uri: Optional[str] = None):
        self.document_uri = document_uri
