from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AverageComparativeScore(ClientValue):
    averageScore: float | None = None
    basis: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AverageComparativeScore"
