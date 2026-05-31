from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CalculatedColumn(ClientValue):
    """The calculatedColumn on a columnDefinition resource indicates that the column's
    data is calculated based on other columns in the site."""

    format: str | None = None
    formula: str | None = None
    outputType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CalculatedColumn"
