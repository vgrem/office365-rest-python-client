from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from office365.delta_collection import DeltaCollection
from office365.directory.permissions.require_permission import require_permission
from office365.outlook.calendar.attendees.attendee import Attendee
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.calendar.events.event import Event
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_value_collection import ClientValueCollection


class EventCollection(DeltaCollection[Event]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, Event, resource_path)

    @require_permission(delegated=["Calendars.ReadWrite"], application=["Calendars.ReadWrite"])
    def add(
        self,
        subject: Optional[str] = None,
        body: Optional[str | ItemBody] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        attendees: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Event:
        """Create an event in the user's default calendar or specified calendar.

        By default, the allowNewTimeProposals property is set to true when an event is created,
        which means invitees can propose a different date/time for the event. See Propose new meeting times
        for more information on how to propose a time, and how to receive and accept a new time proposal.

        Args:
            subject (str): The subject of the message.
            body (str or ItemBody): The body of the message. It can be in HTML or text format
            start (datetime.datetime): The start date, time, and time zone of the event. By default, the start time is in UTC.
            end (datetime.datetime): The date, time, and time zone that the event ends. By default, the end time is in UTC.
            attendees (list[str]): The collection of attendees for the event.
        """

        if body is not None:
            kwargs["body"] = body if isinstance(body, ItemBody) else ItemBody(body)
        if subject is not None:
            kwargs["subject"] = subject
        if start is not None:
            kwargs["start"] = DateTimeTimeZone.parse(start)
        if end is not None:
            kwargs["end"] = DateTimeTimeZone.parse(end)

        if attendees is not None:
            kwargs["attendees"] = ClientValueCollection(
                Attendee,
                [Attendee(EmailAddress(v), type="required") for v in attendees],
            )

        return super().add(**kwargs)
