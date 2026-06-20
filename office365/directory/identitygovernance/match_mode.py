from __future__ import annotations

from enum import Enum


class MatchMode(Enum):
    any = "0"
    all = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.MatchMode"
