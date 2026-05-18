from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.locale_info import LocaleInfo
from office365.runtime.client_value import ClientValue


@dataclass
class AutomaticRepliesMailTips(ClientValue):
    """MailTips about any automatic replies that have been set up on a mailbox."""

    message: str | None = None
    messageLanguage: LocaleInfo = field(default_factory=LocaleInfo)
    scheduledEndTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    scheduledStartTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
