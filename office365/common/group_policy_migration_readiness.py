from __future__ import annotations

from enum import Enum


class GroupPolicyMigrationReadiness(Enum):
    none = "1"
    partial = "2"
    complete = "3"
    error = "4"
    notApplicable = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyMigrationReadiness"
