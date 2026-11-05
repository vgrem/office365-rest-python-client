from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TimeZoneBase(ClientValue):
    """The basic representation of a time zone."""

    name: str | None = None

    def __repr__(self):
        return self.name or ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeZoneBase"
