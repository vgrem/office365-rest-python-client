from __future__ import annotations

from office365.entity import Entity
from office365.partners.billing.billed_reconciliation import BilledReconciliation
from office365.partners.billing.unbilled_reconciliation import UnbilledReconciliation
from office365.runtime.paths.resource_path import ResourcePath


class BillingReconciliation(Entity):
    @property
    def billed(self) -> BilledReconciliation:
        """Gets the billed property"""
        return self.properties.get(
            "billed", BilledReconciliation(self.context, ResourcePath("billed", self.resource_path))
        )

    @property
    def unbilled(self) -> UnbilledReconciliation:
        """Gets the unbilled property"""
        return self.properties.get(
            "unbilled", UnbilledReconciliation(self.context, ResourcePath("unbilled", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.BillingReconciliation"
