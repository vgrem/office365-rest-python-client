from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.agreements.site import SPAgreementsSite


@value
class AgreementsSolutionEnabledSitesResponse(ClientValue):
    Sites: ClientValueCollection[SPAgreementsSite] = field(
        default_factory=lambda: ClientValueCollection(SPAgreementsSite)
    )
    SkipToken: str | None = None
