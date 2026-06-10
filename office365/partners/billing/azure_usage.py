from __future__ import annotations

from office365.entity import Entity
from office365.partners.billing.billed_usage import BilledUsage
from office365.partners.billing.unbilled_usage import UnbilledUsage
from office365.runtime.paths.resource_path import ResourcePath


class AzureUsage(Entity):
    @property
    def billed(self) -> BilledUsage:
        """Gets the billed property"""
        return self.properties.get("billed", BilledUsage(self.context, ResourcePath("billed", self.resource_path)))

    @property
    def unbilled(self) -> UnbilledUsage:
        """Gets the unbilled property"""
        return self.properties.get("unbilled", UnbilledUsage(self.context, ResourcePath("unbilled", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.AzureUsage"
