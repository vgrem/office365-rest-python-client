from __future__ import annotations

from enum import Enum


class RuleOperation(Enum):
    null = "0"
    equals = "1"
    notEquals = "2"
    contains = "3"
    notContains = "4"
    lessThan = "5"
    greaterThan = "6"
    startsWith = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.RuleOperation"
