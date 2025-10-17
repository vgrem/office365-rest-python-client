from enum import Enum


class BookingsAvailabilityStatus(Enum):
    available = "0"
    busy = "1"
    slotsAvailable = "2"
    outOfOffice = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsAvailabilityStatus"
