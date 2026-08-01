from __future__ import annotations

from enum import Enum


class CloudPcOperatingSystem(Enum):
    windows10 = "0"
    windows11 = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcOperatingSystem"
