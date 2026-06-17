from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.dayofweek import DayOfWeek
from office365.outlook.mail.recurrencepatterntype import RecurrencePatternType
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class RecurrencePattern(ClientValue):
    """Describes the frequency by which a recurring event repeats."""

    dayOfMonth: int | None = None
    daysOfWeek: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(DayOfWeek))
    firstDayOfWeek: DayOfWeek | None = None
    index: int | None = None
    interval: int | None = None
    month: int | None = None
    type: RecurrencePatternType | None = None
