from __future__ import annotations

from enum import Enum


class RecoveryAction(Enum):
    softDelete = "0"
    update = "1"
    restore = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryAction"
