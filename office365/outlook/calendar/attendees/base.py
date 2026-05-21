from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.outlook.calendar.email_address import EmailAddress
from office365.outlook.mail.recipient import Recipient


@dataclass
class AttendeeBase(Recipient):
    """The type of attendees."""

    type: str | None = None
