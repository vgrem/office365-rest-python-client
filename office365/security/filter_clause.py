from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.filter_operand import FilterOperand


@value
class FilterClause(ClientValue):
    operatorName: str | None = None
    sourceOperandName: str | None = None
    targetOperand: FilterOperand = field(default_factory=FilterOperand)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FilterClause"
