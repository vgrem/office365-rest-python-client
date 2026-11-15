from enum import Enum


class BookingStaffMembershipStatus(Enum):
    active = "0"
    pendingAcceptance = "1"
    rejectedByStaff = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingStaffMembershipStatus"
