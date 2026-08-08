from __future__ import annotations

from enum import Enum


class BinaryOperator(Enum):
    or_ = "0"
    and_ = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BinaryOperator"
