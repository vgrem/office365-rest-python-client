from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.identitygovernance.quarantine_type import QuarantineType
from office365.runtime.client_value import ClientValue


@dataclass
class QuarantineDetails(ClientValue):
    quarantinedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    quarantineReason: str | None = None
    quarantineType: QuarantineType = QuarantineType.notQuarantined

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.QuarantineDetails"
