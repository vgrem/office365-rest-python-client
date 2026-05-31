from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class WebPartPosition(ClientValue):
    columnId: float | None = None
    horizontalSectionId: float | None = None
    isInVerticalSection: bool | None = None
    webPartIndex: float | None = None
    "Represents the position information of the given web part to the current page"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebPartPosition"
