from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.expirationpatterntype import (
    ExpirationPatternType,
)
from office365.runtime.client_value import ClientValue


@dataclass
class ExpirationPattern(ClientValue):
    duration: timedelta | None = None
    endDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    type: ExpirationPatternType = ExpirationPatternType.notSpecified

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExpirationPattern"
