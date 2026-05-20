from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Sort(ClientValue):
    """Contains information about the property to sort the search results on, and how to sort on the property."""

    Direction: int | None = None
    Property: str | None = None

    def __str__(self):
        return f"{self.Property}:{self.Direction}"

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.Sort"
