from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.datapair import AgreementDataPair


@dataclass
class AgreementReportBaseData(ClientValue):
    by_expiration_status: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    error_message: Optional[str] = None
    expired: Optional[int] = None
    in_effect: Optional[int] = None
    in_progress_by_state: ClientValueCollection[AgreementDataPair] = field(
        default_factory=lambda: ClientValueCollection(AgreementDataPair)
    )
    near_expiration: Optional[int] = None
