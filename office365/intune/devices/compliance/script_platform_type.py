from __future__ import annotations

from enum import Enum


class DeviceComplianceScriptPlatformType(Enum):
    windows10 = "0"
    linux = "1"
    macOS = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceComplianceScriptPlatformType"
