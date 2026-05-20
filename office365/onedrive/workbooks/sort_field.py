from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.workbooks.icon import WorkbookIcon
from office365.runtime.client_value import ClientValue


@dataclass
class WorkbookSortField(ClientValue):
    """Represents a condition in a sorting operation."""

    ascending: bool | None = None
    color: str | None = None
    dataOption: str | None = None
    icon: WorkbookIcon | None = field(default_factory=WorkbookIcon)
    key: str | None = None
