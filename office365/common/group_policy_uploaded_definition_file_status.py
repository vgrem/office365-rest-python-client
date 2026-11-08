from __future__ import annotations

from enum import Enum


class GroupPolicyUploadedDefinitionFileStatus(Enum):
    none = "0"
    uploadInProgress = "1"
    available = "2"
    assigned = "3"
    removalInProgress = "4"
    uploadFailed = "5"
    removalFailed = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyUploadedDefinitionFileStatus"
