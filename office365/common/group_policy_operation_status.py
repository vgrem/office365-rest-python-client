from __future__ import annotations

from enum import Enum


class GroupPolicyOperationStatus(Enum):
    unknown = "0"
    inProgress = "1"
    success = "2"
    failed = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyOperationStatus"
