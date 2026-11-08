from __future__ import annotations

from enum import Enum


class GroupPolicyConfigurationIngestionType(Enum):
    unknown = "0"
    custom = "1"
    builtIn = "2"
    mixed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyConfigurationIngestionType"
