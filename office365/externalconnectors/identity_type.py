from __future__ import annotations

from enum import Enum


class IdentityType(Enum):
    user = "1"
    group = "2"
    externalGroup = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.IdentityType"
