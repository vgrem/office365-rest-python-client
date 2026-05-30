from __future__ import annotations

from enum import Enum


class HoldType(Enum):
    none = "0"
    private = "1"
    public = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HoldType"
