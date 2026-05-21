from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.teams.schedule.shifts.time_range import TimeRange


@dataclass
class ShiftAvailability(ClientValue):
    """Availability of the user to be scheduled for a shift and its recurrence pattern."""

    recurrence: PatternedRecurrence = field(default_factory=PatternedRecurrence)
    timeSlots: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(TimeRange))
    timeZone: str | None = None
