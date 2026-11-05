from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RecommendedAction(ClientValue):
    actionWebUrl: str | None = None
    potentialScoreImpact: float | None = None
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RecommendedAction"
