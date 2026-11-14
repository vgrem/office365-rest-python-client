from __future__ import annotations

from enum import Enum


class ManagedAppDeviceThreatLevel(Enum):
    notConfigured = "0"
    secured = "1"
    low = "2"
    medium = "3"
    high = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAppDeviceThreatLevel"
