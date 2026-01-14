from office365.runtime.client_value import ClientValue


class ReviewerInfo(ClientValue):
    def __init__(self, email: str = None, name: str = None, reviewer_id: int = None):
        self.Email = email
        self.Name = name
        self.ReviewerId = reviewer_id
