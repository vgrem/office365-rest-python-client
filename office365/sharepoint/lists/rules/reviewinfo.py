from typing import Optional

from office365.runtime.client_value import ClientValue


class ReviewerInfo(ClientValue):
    def __init__(self, email: Optional[str] = None, name: Optional[str] = None, reviewer_id: Optional[int] = None):
        self.Email = email
        self.Name = name
        self.ReviewerId = reviewer_id
