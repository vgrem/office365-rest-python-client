from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WebPartPosition(ClientValue):
    columnId: float | None = None
    horizontalSectionId: float | None = None
    isInVerticalSection: bool | None = None
    webPartIndex: float | None = None
    "Represents the position information of the given web part to the current page"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebPartPosition"
