from __future__ import annotations

from enum import Enum


class AttributeSet(Enum):
    full = "1"
    basic = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.AttributeSet"
