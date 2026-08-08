from __future__ import annotations

from enum import Enum


class AclType(Enum):
    user = "1"
    group = "2"
    everyone = "3"
    everyoneExceptGuests = "4"
    externalGroup = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.AclType"
