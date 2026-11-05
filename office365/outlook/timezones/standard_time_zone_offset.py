from __future__ import annotations

from datetime import time

from office365.outlook.calendar.dayofweek import DayOfWeek
from office365.runtime.client_value import ClientValue


class StandardTimeZoneOffset(ClientValue):
    dayOccurrence: int | None = None
    dayOfWeek: DayOfWeek = DayOfWeek.sunday
    month: int | None = None
    time: time | None = None
    year: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StandardTimeZoneOffset"
