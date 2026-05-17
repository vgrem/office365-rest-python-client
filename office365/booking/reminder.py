from __future__ import annotations

from datetime import timedelta
from typing import Optional

from office365.booking.reminderrecipients import BookingReminderRecipients
from office365.runtime.client_value import ClientValue


class BookingReminder(ClientValue):
    def __init__(
        self,
        message: Optional[str] = None,
        offset: Optional[timedelta] = None,
        recipients: Optional[BookingReminderRecipients] = None,
    ):
        self.message = message
        self.offset = offset
        self.recipients = recipients

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingReminder"
