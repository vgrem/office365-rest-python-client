from __future__ import annotations

from enum import Enum


class ScopeCollectionKind(Enum):
    allAllowed = "0"
    enumerated = "1"
    none = "2"
    scopeKindNotSet = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ScopeCollectionKind"
