from __future__ import annotations

from enum import Enum


class DetectionRuleStatus(Enum):
    enabled = "0"
    disabled = "1"
    autoDisabled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DetectionRuleStatus"
