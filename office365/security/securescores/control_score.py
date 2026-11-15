from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ControlScore(ClientValue):
    controlCategory: str | None = None
    controlName: str | None = None
    description: str | None = None
    score: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ControlScore"
