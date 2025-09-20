from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.actionablemessages.user import UserDTO


class AgreementAttributeDTO(ClientValue):

    def __init__(
        self,
        review_complete_date: datetime = None,
        reviewer: UserDTO = UserDTO(),
        review_id: str = None,
        review_start_date: datetime = None,
        state: int = None,
    ):
        self.review_complete_date = review_complete_date
        self.reviewer = reviewer
        self.review_id = review_id
        self.review_start_date = review_start_date
        self.state = state
