from __future__ import annotations

from enum import Enum


class QuarantineType(Enum):
    notQuarantined = "0"
    countBasedThresholdExceeded = "1"
    percentageBasedThresholdExceeded = "2"
    multipleConditionsExceeded = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.QuarantineType"
