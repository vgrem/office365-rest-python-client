from enum import Enum


class BookingReminderRecipients(Enum):
    allAttendees = "0"
    staff = "1"
    customer = "2"
    unknownFutureValue = "3"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingReminderRecipients"
