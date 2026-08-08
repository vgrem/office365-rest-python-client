from __future__ import annotations

from enum import Enum


class PstnCallDurationSource(Enum):
    microsoft = "0"
    operator = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.PstnCallDurationSource"
