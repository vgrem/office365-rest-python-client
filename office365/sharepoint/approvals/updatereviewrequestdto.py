from typing import Optional

from office365.runtime.client_value import ClientValue


class UpdateReviewRequestDTO(ClientValue):
    def __init__(
        self,
        action: Optional[str] = None,
        comments: Optional[str] = None,
        document_uri: Optional[str] = None,
        reviewer_email_or_upn: Optional[str] = None,
    ):
        self.action = action
        self.comments = comments
        self.document_uri = document_uri
        self.reviewer_email_or_upn = reviewer_email_or_upn
