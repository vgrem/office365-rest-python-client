from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationPlatforms(Enum):
    none = "0"
    android = "1"
    iOS = "4"
    macOS = "8"
    windows10X = "16"
    windows10 = "32"
    linux = "128"
    unknownFutureValue = "256"
    androidEnterprise = "512"
    aosp = "1024"
    visionOS = "2048"
    tvOS = "4096"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationPlatforms"
