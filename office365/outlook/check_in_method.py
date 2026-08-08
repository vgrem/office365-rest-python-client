from __future__ import annotations

from enum import Enum


class CheckInMethod(Enum):
    unspecified = "0"
    manual = "1"
    inferred = "2"
    verified = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CheckInMethod"
