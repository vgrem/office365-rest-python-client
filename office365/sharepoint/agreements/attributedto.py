from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.approvals.user import UserDTO


class AgreementAttributeDTO(ClientValue):
    def __init__(
        self,
        review_complete_date: Optional[datetime] = None,
        reviewer: UserDTO = UserDTO(),
        review_id: Optional[str] = None,
        review_start_date: Optional[datetime] = None,
        state: Optional[int] = None,
    ):
        self.review_complete_date = review_complete_date
        self.reviewer = reviewer
        self.review_id = review_id
        self.review_start_date = review_start_date
        self.state = state
