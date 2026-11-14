from __future__ import annotations

from enum import Enum


class DeviceCustomAttributeValueType(Enum):
    integer = "0"
    string = "1"
    dateTime = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceCustomAttributeValueType"
