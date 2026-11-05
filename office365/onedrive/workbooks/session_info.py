from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WorkbookSessionInfo(ClientValue):
    """Provides information about workbook session."""

    persistChanges: bool | None = None
    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookSessionInfo"
