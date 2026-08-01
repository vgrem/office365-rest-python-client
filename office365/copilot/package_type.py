from __future__ import annotations

from enum import Enum


class PackageType(Enum):
    microsoft = "0"
    external = "1"
    shared = "2"
    custom = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PackageType"
