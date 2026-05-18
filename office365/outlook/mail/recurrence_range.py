from __future__ import annotations

import datetime
from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RecurrenceRange(ClientValue):
    """
    Describes a date range over which a recurring event. This shared hobject is used to define the recurrence
    of access reviews, calendar events, and access package assignments in Azure AD.
    """

    endDate: datetime.date | None = None
    numberOfOccurrences: int | None = None
    recurrenceTimeZone: str | None = None
    startDate: datetime.date | None = None
    type: str | None = None
