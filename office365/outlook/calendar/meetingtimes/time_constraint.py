from __future__ import annotations

from dataclasses import field

from office365.outlook.calendar.meetingtimes.time_slot import TimeSlot
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class TimeConstraint(ClientValue):
    """Restricts meeting time suggestions to certain hours and days of the week according to the specified nature of
    activity and open time slots."""

    activityDomain: str | None = None
    timeSlots: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(TimeSlot))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeConstraint"
