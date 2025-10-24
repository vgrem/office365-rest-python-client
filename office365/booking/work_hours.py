from typing import List

from office365.booking.work_time_slot import BookingWorkTimeSlot
from office365.outlook.calendar.dayofweek import DayOfWeek
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingWorkHours(ClientValue):
    """Represents the set of working hours in a single day of the week, for a bookingBusiness or bookingStaffMember."""

    def __init__(self, day: DayOfWeek = None, time_slots: List[BookingWorkTimeSlot] = None):
        """
        :param DayOfWeek day: The day of the week represented by this instance.
            Possible values are: sunday, monday, tuesday, wednesday, thursday, friday, saturday.
        :param list[BookingWorkTimeSlot] time_slots: A list of start/end times during a day.
        """
        self.day = day
        self.timeSlots = ClientValueCollection(BookingWorkTimeSlot, time_slots)

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingWorkHours"
