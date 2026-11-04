from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DateTimeColumn(ClientValue):
    """The dateTimeColumn on a columnDefinition resource indicates that the column's values are dates or times."""

    displayAs: str | None = None
    format: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DateTimeColumn"
