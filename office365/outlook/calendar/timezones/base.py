from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TimeZoneBase(ClientValue):
    """The basic representation of a time zone."""

    name: str | None = None

    def __repr__(self):
        return self.name or ""
