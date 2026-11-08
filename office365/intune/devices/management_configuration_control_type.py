from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationControlType(Enum):
    default = "0"
    dropdown = "1"
    smallTextBox = "2"
    largeTextBox = "3"
    toggle = "4"
    multiheaderGrid = "5"
    contextPane = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationControlType"
