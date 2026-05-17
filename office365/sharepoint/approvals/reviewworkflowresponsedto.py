from typing import Optional

from office365.runtime.client_value import ClientValue


class ReviewWorkFlowResponseDTO(ClientValue):
    def __init__(self, action: Optional[str] = None, comments: Optional[str] = None, status: Optional[str] = None):
        self.action = action
        self.comments = comments
        self.status = status
