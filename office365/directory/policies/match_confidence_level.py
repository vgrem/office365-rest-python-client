from __future__ import annotations

from enum import Enum


class MatchConfidenceLevel(Enum):
    exact = "0"
    relaxed = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MatchConfidenceLevel"
