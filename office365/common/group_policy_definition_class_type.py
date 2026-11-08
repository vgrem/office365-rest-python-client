from __future__ import annotations

from enum import Enum


class GroupPolicyDefinitionClassType(Enum):
    user = "0"
    machine = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyDefinitionClassType"
