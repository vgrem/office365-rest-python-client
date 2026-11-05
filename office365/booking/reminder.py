from __future__ import annotations

from datetime import timedelta

from office365.booking.reminderrecipients import BookingReminderRecipients
from office365.runtime.client_value import ClientValue


class BookingReminder(ClientValue):
    message: str | None = None
    offset: timedelta | None = None
    recipients: BookingReminderRecipients | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingReminder"
