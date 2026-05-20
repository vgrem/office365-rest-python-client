from __future__ import annotations

from dataclasses import dataclass
from typing import List

from office365.booking.work_time_slot import BookingWorkTimeSlot
from office365.outlook.calendar.dayofweek import DayOfWeek
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class BookingWorkHours(ClientValue):
    """Represents the set of working hours in a single day of the week, for a bookingBusiness or bookingStaffMember.

    Fields:
        day: The day of the week. Possible values: sunday, monday, tuesday, wednesday, thursday, friday, saturday.
        timeSlots: A list of start/end times during a day.
    """

    day: DayOfWeek | None = None
    timeSlots: List[BookingWorkTimeSlot] | None = None

    def __post_init__(self) -> None:
        if self.timeSlots is not None:
            self.timeSlots = ClientValueCollection(BookingWorkTimeSlot, self.timeSlots)  # type: ignore[assignment]

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BookingWorkHours"
