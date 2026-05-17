from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementReportFilter(ClientValue):
    def __init__(
        self,
        category: Optional[str] = None,
        first_party: Optional[str] = None,
        language: Optional[str] = None,
        location: Optional[str] = None,
        owner: Optional[str] = None,
        second_party: Optional[str] = None,
        state: Optional[str] = None,
    ):
        self.category = category
        self.first_party = first_party
        self.language = language
        self.location = location
        self.owner = owner
        self.second_party = second_party
        self.state = state
