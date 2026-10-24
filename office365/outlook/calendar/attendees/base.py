from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.recipient import Recipient
from office365.runtime.types.odata_property import Compare, odata


@dataclass
class AttendeeBase(Recipient):
    """The type of attendees."""

    #: An attendee with no type is a required one.
    type: str | None = field(default=None, metadata=odata("type", compare=Compare(default="required")))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttendeeBase"
