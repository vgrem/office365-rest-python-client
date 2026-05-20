from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DateTimeColumn(ClientValue):
    """The dateTimeColumn on a columnDefinition resource indicates that the column's values are dates or times."""

    displayAs: str | None = None
    format: str | None = None
