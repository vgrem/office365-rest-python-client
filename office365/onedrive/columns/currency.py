from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CurrencyColumn(ClientValue):
    """The currencyColumn on a columnDefinition resource indicates that the column's values represent currency."""

    locale: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CurrencyColumn"
