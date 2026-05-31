from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class NumberColumn(ClientValue):
    """The numberColumn on a columnDefinition resource indicates that the column's values are numbers."""

    minimum: float | None = None
    maximum: float | None = None
    displayAs: str | None = None
    decimalPlaces: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NumberColumn"
