from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.site import SPAgreementsSite


@dataclass
class AgreementsSolutionEnabledSitesResponse(ClientValue):
    sites: Optional[ClientValueCollection[SPAgreementsSite]] = None
    skip_token: Optional[str] = None
