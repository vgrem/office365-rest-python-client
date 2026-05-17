from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementSearchParameters(ClientValue):
    def __init__(
        self,
        agreement_number: Optional[str] = None,
        category: Optional[str] = None,
        owner: Optional[str] = None,
        row_limit: Optional[int] = None,
        start_row: Optional[int] = None,
        state: Optional[str] = None,
    ):
        self.agreement_number = agreement_number
        self.category = category
        self.owner = owner
        self.row_limit = row_limit
        self.start_row = start_row
        self.state = state
