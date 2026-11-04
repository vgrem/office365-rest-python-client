from __future__ import annotations

from dataclasses import field

from office365.onedrive.workbooks.icon import WorkbookIcon
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WorkbookSortField(ClientValue):
    """Represents a condition in a sorting operation."""

    ascending: bool | None = None
    color: str | None = None
    dataOption: str | None = None
    icon: WorkbookIcon | None = field(default_factory=WorkbookIcon)
    key: str | None = None
    sortOn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookSortField"
