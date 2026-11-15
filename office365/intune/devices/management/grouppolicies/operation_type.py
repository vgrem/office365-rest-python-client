from __future__ import annotations

from enum import Enum


class GroupPolicyOperationType(Enum):
    none = "0"
    upload = "1"
    uploadNewVersion = "2"
    addLanguageFiles = "3"
    removeLanguageFiles = "4"
    updateLanguageFiles = "5"
    remove = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyOperationType"
