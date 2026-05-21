from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class Certification(ClientValue):
    """Represents the certification details of an application.

    :param str certification_details_url:
    """

    certificationDetailsUrl: str | None = None
    certificationExpirationDateTime: datetime | None = None
    isCertifiedByMicrosoft: bool | None = None
    isPublisherAttested: bool | None = None
    lastCertificationDateTime: datetime | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Certification"
