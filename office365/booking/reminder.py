from datetime import timedelta

from office365.booking.reminderrecipients import BookingReminderRecipients
from office365.runtime.client_value import ClientValue


class BookingReminder(ClientValue):

    def __init__(
        self,
        message: str = None,
        offset: timedelta = None,
        recipients: BookingReminderRecipients = BookingReminderRecipients.none,
    ):
        self.message = message
        self.offset = offset
        self.recipients = recipients

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingReminder"
