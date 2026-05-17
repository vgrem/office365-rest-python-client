from enum import Enum


class BillingPeriod(Enum):
    current = "1"
    last = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.partners.billing.BillingPeriod"
