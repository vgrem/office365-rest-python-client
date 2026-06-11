from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.datapair import AgreementDataPair


@dataclass
class AgreementReportBaseData(ClientValue):
    ByExpirationStatus: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    ErrorMessage: str | None = None
    Expired: int | None = None
    InEffect: int | None = None
    InProgressByState: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    NearExpiration: int | None = None
