from __future__ import annotations

from enum import Enum


class RemediationState(Enum):
    unknown = "0"
    skipped = "1"
    success = "2"
    remediationFailed = "3"
    scriptError = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RemediationState"
