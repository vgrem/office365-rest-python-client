from enum import Enum


class VirtualEventAttendeeRegistrationStatus(Enum):
    registered = "0"
    canceled = "1"
    waitlisted = "2"
    pendingApproval = "3"
    rejectedByOrganizer = "4"
    unknownFutureValue = "11"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VirtualEventAttendeeRegistrationStatus"
