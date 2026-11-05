from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.datapair import AgreementDataPair


class AgreementSummaryData(ClientValue):
    by_category: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    by_expiration_year: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    by_first_party: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    by_renewal_year: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    by_second_party: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
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
