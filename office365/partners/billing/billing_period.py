from __future__ import annotations

from enum import Enum


class BillingPeriod(Enum):
    current = "1"
    last = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.BillingPeriod"
