from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class WorkbookFilterCriteria(ClientValue):
    """Represents the filtering criteria applied to a column."""

    color: str | None = None
    dynamicCriteria: str | None = None
    operator: str | None = None
    values: list | None = field(default_factory=list)
