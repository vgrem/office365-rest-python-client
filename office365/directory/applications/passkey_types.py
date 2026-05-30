from __future__ import annotations

from enum import Enum


class PasskeyTypes(Enum):
    deviceBound = "1"
    synced = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PasskeyTypes"
