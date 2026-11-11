from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.partners.billing.operation import Operation


class BilledAggregatedUsage(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.BilledAggregatedUsage"

    @require_permission(delegated=["PartnerBilling.Read.All"], application=["PartnerBilling.Read.All"])
    def export(self, invoice_id: str) -> Operation:
        """export operation.

        Args:
            invoice_id (str):
                invoiceId parameter
        """
        from office365.partners.billing.operation import Operation

        return_type = Operation(self.context)
        qry = ServiceOperationQuery(self, "export", None, {"invoiceId": invoice_id}, None, return_type)
        self.context.add_query(qry)
        return return_type
