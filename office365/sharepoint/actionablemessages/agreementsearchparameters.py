from office365.runtime.client_value import ClientValue


class AgreementSearchParameters(ClientValue):

    def __init__(
        self,
        agreement_number: str = None,
        category: str = None,
        owner: str = None,
        row_limit: int = None,
        start_row: int = None,
        state: str = None,
    ):
        self.agreement_number = agreement_number
        self.category = category
        self.owner = owner
        self.row_limit = row_limit
        self.start_row = start_row
        self.state = state
