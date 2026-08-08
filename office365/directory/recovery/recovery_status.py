from __future__ import annotations

from enum import Enum


class RecoveryStatus(Enum):
    initialized = "0"
    running = "1"
    successful = "2"
    failed = "3"
    abandoned = "4"
    unknownFutureValue = "5"
    calculating = "6"
    loadingData = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryStatus"
