from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.location import Location
from office365.runtime.client_value import ClientValue


@dataclass
class Reminder(ClientValue):
    """A reminder for an event in a user calendar.

    Fields:
        changeKey (str | None): Identifies the version of the reminder. Every time the reminder is changed, changeKey
            changes as well. This allows Exchange to apply changes to the correct version of the object.
        eventStartTime (DateTimeTimeZone): The date, time, and time zone that the event starts.
        eventEndTime (DateTimeTimeZone): The date, time and time zone that the event ends.
        eventId (str | None): The unique ID of the event. Read only.
        eventLocation (Location): The location of the event.
        eventSubject (str | None): The text of the event's subject line.
        eventWebLink (str | None): The URL to open the event in Outlook on the web.
            The event will open in the browser if you are logged in to your mailbox via Outlook on the web.
            You will be prompted to login if you are not already logged in with the browser.
            This URL cannot be accessed from within an iFrame.
        reminderFireTime (DateTimeTimeZone): The date, time, and time zone that the reminder is set to occur.
    """

    changeKey: str | None = None
    eventEndTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    eventId: str | None = None
    eventLocation: Location = field(default_factory=Location)
    eventStartTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    eventSubject: str | None = None
    eventWebLink: str | None = None
    reminderFireTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
