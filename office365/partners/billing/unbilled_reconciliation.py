from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.partners.billing.attribute_set import AttributeSet
    from office365.partners.billing.operation import Operation
    from office365.partners.billing.period import BillingPeriod


class UnbilledReconciliation(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.UnbilledReconciliation"

    def export(self, currency_code: str, billing_period: BillingPeriod, attribute_set: AttributeSet) -> Operation:
        """export operation.

        Args:
            currency_code (str):
                currencyCode parameter
            billing_period (BillingPeriod):
                billingPeriod parameter
            attribute_set (AttributeSet):
                attributeSet parameter
        """
        from office365.partners.billing.operation import Operation

        return_type = Operation(self.context)
        qry = ServiceOperationQuery(
            self,
            "export",
            None,
            {"currencyCode": currency_code, "billingPeriod": billing_period, "attributeSet": attribute_set},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
