from __future__ import annotations

from enum import Enum


class DeviceHealthScriptType(Enum):
    deviceHealthScript = "0"
    managedInstallerScript = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceHealthScriptType"
