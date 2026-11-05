from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WorkbookIcon(ClientValue):
    index: int | None = None
    set: str | None = None
    "Represents a cell icon."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookIcon"
