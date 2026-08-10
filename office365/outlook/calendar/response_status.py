from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class ResponseStatus(ClientValue):
    """Represents the response status of an attendee or organizer for a meeting request.

    Fields:
        response (str | None): The response status.
    """

    response: str | None = None
    time: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResponseStatus"
