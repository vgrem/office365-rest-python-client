from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.filter_operand import FilterOperand
from office365.runtime.client_value import ClientValue


@dataclass
class FilterClause(ClientValue):
    operatorName: str | None = None
    sourceOperandName: str | None = None
    targetOperand: FilterOperand = field(default_factory=FilterOperand)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FilterClause"
