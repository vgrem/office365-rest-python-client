from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.partners.billing.billed_aggregated_usage import BilledAggregatedUsage


class AzureAggregatedUsage(Entity):
    @odata(name="billed", navigation=True)
    @property
    def billed(self) -> BilledAggregatedUsage:
        """Gets the billed property"""
        from office365.partners.billing.billed_aggregated_usage import BilledAggregatedUsage

        return self.properties.get(
            "billed", BilledAggregatedUsage(self.context, ResourcePath("billed", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.AzureAggregatedUsage"
