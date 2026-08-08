from __future__ import annotations

from enum import Enum


class VerifiedIdUsageConfigurationPurpose(Enum):
    recovery = "0"
    onboarding = "1"
    all = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VerifiedIdUsageConfigurationPurpose"
