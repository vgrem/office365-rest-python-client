from office365.runtime.client_value import ClientValue


class UpdateReviewRequestDTO(ClientValue):

    def __init__(
        self,
        action: str = None,
        comments: str = None,
        document_uri: str = None,
        reviewer_email_or_upn: str = None,
    ):
        self.action = action
        self.comments = comments
        self.document_uri = document_uri
        self.reviewer_email_or_upn = reviewer_email_or_upn
