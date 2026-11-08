from __future__ import annotations

from enum import Enum


class GroupPolicySettingScope(Enum):
    unknown = "0"
    device = "1"
    user = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicySettingScope"
