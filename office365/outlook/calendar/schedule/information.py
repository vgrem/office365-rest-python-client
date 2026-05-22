from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.schedule.item import ScheduleItem
from office365.outlook.calendar.working_hours import WorkingHours
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ScheduleInformation(ClientValue):
    """Represents the availability of a user, distribution list, or resource (room or equipment)
    for a specified time period."""

    scheduleItems: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(ScheduleItem))
    scheduleId: str | None = None
    availabilityView: str | None = None
    error: str | None = None
    workingHours: WorkingHours = field(default_factory=WorkingHours)
