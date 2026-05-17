from enum import Enum


class BookingsServiceAvailabilityType(Enum):
    bookWhenStaffAreFree = "0"
    notBookable = "1"
    customWeeklyHours = "2"
    unknownFutureValue = "3"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsServiceAvailabilityType"
