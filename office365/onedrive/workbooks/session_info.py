from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class WorkbookSessionInfo(ClientValue):
    """Provides information about workbook session."""

    persistChanges: bool | None = None
    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookSessionInfo"
