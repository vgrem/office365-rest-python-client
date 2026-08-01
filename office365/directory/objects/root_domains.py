from __future__ import annotations

from enum import Enum


class RootDomains(Enum):
    none = "0"
    all = "1"
    allFederated = "2"
    allManaged = "3"
    enumerated = "4"
    allManagedAndEnumeratedFederated = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RootDomains"
