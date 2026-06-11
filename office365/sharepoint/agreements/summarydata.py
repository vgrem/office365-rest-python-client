from __future__ import annotations

from dataclasses import dataclass, field
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
    ByCategory: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    ByExpirationYear: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    ByFirstParty: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    ByRenewalYear: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    BySecondParty: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    Evergreen: int | None = None
