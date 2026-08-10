from __future__ import annotations

from dataclasses import dataclass

from office365.outlook.mail.recipient import Recipient


@dataclass
class AttendeeBase(Recipient):
    """The type of attendees."""

    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttendeeBase"
