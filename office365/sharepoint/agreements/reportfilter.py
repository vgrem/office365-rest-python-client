from office365.runtime.client_value import ClientValue


class AgreementReportFilter(ClientValue):

    def __init__(
        self,
        category: str = None,
        first_party: str = None,
        language: str = None,
        location: str = None,
        owner: str = None,
        second_party: str = None,
        state: str = None,
    ):
        self.category = category
        self.first_party = first_party
        self.language = language
        self.location = location
        self.owner = owner
        self.second_party = second_party
        self.state = state
