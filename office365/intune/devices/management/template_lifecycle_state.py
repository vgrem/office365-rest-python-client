from __future__ import annotations

from enum import Enum


class DeviceManagementTemplateLifecycleState(Enum):
    invalid = "0"
    draft = "10"
    active = "20"
    superseded = "30"
    deprecated = "40"
    retired = "50"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementTemplateLifecycleState"
