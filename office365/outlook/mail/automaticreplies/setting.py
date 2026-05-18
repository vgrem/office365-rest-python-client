from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue


@dataclass
class AutomaticRepliesSetting(ClientValue):
    """
    Configuration settings to automatically notify the sender of an incoming email with a message from the signed-in
    user. For example, an automatic reply to notify that the signed-in user is unavailable to respond to emails.
    """

    externalAudience: str | None = None
    externalReplyMessage: str | None = None
    internalReplyMessage: str | None = None
    scheduledEndDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    scheduledStartDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    status: str | None = None
