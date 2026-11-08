from __future__ import annotations

from enum import Enum


class GroupPolicyType(Enum):
    admxBacked = "0"
    admxIngested = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyType"
