from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue


@dataclass
class FollowupFlag(ClientValue):
    """Allows setting a flag in an item for the user to follow up on later.

    Fields:
        completedDateTime: The date and time that the follow-up was finished.
        dueDateTime: The date and time that the follow up is to be finished.
            Note: To set the due date, you must also specify the startDateTime;
            otherwise, you will get a 400 Bad Request response.
        flagStatus: The status for follow-up for an item.
        startDateTime: The date and time that the follow-up is to begin.
    """

    completedDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    dueDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    flagStatus: str | None = None
    startDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
