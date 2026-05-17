from enum import Enum


class BookingStaffRole(Enum):
    guest = "0"
    administrator = "1"
    viewer = "2"
    externalGuest = "3"
    unknownFutureValue = "4"
    scheduler = "5"
    teamMember = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingStaffRole"
