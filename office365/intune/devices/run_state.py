from __future__ import annotations

from enum import Enum


class RunState(Enum):
    unknown = "0"
    success = "1"
    fail = "2"
    scriptError = "3"
    pending = "4"
    notApplicable = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RunState"
