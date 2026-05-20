from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.datapair import AgreementDataPair


@dataclass
class AgreementSummaryData(ClientValue):
    by_category: Optional[ClientValueCollection[AgreementDataPair]] = None
    by_expiration_year: Optional[ClientValueCollection[AgreementDataPair]] = None
    by_first_party: Optional[ClientValueCollection[AgreementDataPair]] = None
    by_renewal_year: Optional[ClientValueCollection[AgreementDataPair]] = None
    by_second_party: Optional[ClientValueCollection[AgreementDataPair]] = None
    evergreen: Optional[int] = None
