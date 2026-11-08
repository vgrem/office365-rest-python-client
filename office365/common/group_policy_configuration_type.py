from __future__ import annotations

from enum import Enum


class GroupPolicyConfigurationType(Enum):
    policy = "0"
    preference = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyConfigurationType"
