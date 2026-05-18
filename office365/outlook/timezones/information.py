from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TimeZoneInformation(ClientValue):
    """Represents a time zone. The supported format is Windows, and Internet Assigned Numbers Authority (IANA)
    time zone (also known as Olson time zone) format as well when the current known problem is fixed.

    Fields:
        alias (str | None): An identifier for the time zone.
        displayName (str | None): A display string that represents the time zone.
    """

    alias: str | None = None
    displayName: str | None = None

    def __repr__(self) -> str:
        return self.displayName or ""
