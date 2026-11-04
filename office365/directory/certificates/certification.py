from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Certification(ClientValue):
    """Represents the certification details of an application.

    Args:
        certification_details_url (str):
    """

    certificationDetailsUrl: str | None = None
    certificationExpirationDateTime: datetime | None = None
    isCertifiedByMicrosoft: bool | None = None
    isPublisherAttested: bool | None = None
    lastCertificationDateTime: datetime | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Certification"
