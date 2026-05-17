from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.datapair import AgreementDataPair


class AgreementSummaryData(ClientValue):
    def __init__(
        self,
        by_category: Optional[ClientValueCollection[AgreementDataPair]] = None,
        by_expiration_year: Optional[ClientValueCollection[AgreementDataPair]] = None,
        by_first_party: Optional[ClientValueCollection[AgreementDataPair]] = None,
        by_renewal_year: Optional[ClientValueCollection[AgreementDataPair]] = None,
        by_second_party: Optional[ClientValueCollection[AgreementDataPair]] = None,
        evergreen: Optional[int] = None,
    ):
        self.by_category = by_category
        self.by_expiration_year = by_expiration_year
        self.by_first_party = by_first_party
        self.by_renewal_year = by_renewal_year
        self.by_second_party = by_second_party
        self.evergreen = evergreen
