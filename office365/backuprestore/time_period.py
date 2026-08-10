from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class TimePeriod(ClientValue):
    endDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    startDateTime: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimePeriod"
