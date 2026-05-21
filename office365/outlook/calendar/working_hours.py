from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.timezones.base import TimeZoneBase
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class WorkingHours(ClientValue):
    """
    Represents the days of the week and hours in a specific time zone that the user works.

    Having access to a user's working hours is useful in scenarios that handle activity or resource planning.
    You can get and set the working hours of a user as part of the user's mailbox settings.

    You can choose to set a time zone for your working hours differently from the time zone you have set on your
    Outlook client. This can be useful in cases like when you travel to a different time zone than you usually work in.
    You can set the Outlook client to the destination time zone so that Outlook time values are displayed in local
    time while you are there. When other people request work meetings with you in your usual place of work,
    they can still respect your working hours in the appropriate time zone.
    """

    daysOfWeek: StringCollection = field(default_factory=StringCollection)
    timeZone: TimeZoneBase = field(default_factory=TimeZoneBase)
    endTime: str | None = None
    startTime: str | None = None
