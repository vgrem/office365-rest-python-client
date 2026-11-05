from __future__ import annotations

from dataclasses import field
from datetime import datetime, timedelta

from office365.runtime.client_value import ClientValue


class TermsExpiration(ClientValue):
    frequency: timedelta | None = None
    startDateTime: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TermsExpiration"
