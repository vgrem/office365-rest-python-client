from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.partners.billing.attribute_set import AttributeSet
    from office365.partners.billing.operation import Operation


class BilledReconciliation(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.BilledReconciliation"

    def export(self, invoice_id: str, attribute_set: AttributeSet) -> Operation:
        """export operation.

        Args:
            invoice_id (str):
                invoiceId parameter
            attribute_set (AttributeSet):
                attributeSet parameter
        """
        from office365.partners.billing.operation import Operation

        return_type = Operation(self.context)
        qry = ServiceOperationQuery(
            self, "export", None, {"invoiceId": invoice_id, "attributeSet": attribute_set}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
