from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ResponseStatus(ClientValue):
    """Represents the response status of an attendee or organizer for a meeting request.

    Fields:
        response (str | None): The response status.
    """

    response: str | None = None
