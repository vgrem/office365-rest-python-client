from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class SigningCertificateUpdateStatus(ClientValue):
    certificateUpdateResult: str | None = None
    lastRunDateTime: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SigningCertificateUpdateStatus"
