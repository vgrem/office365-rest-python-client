from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.multi_tenant_application_metrics_initial import (
        MultiTenantApplicationMetricsInitial,
    )
    from office365.directory.multi_tenant_application_metrics_recent import (
        MultiTenantApplicationMetricsRecent,
    )


class MultiTenantApplicationMetrics(Entity):
    @odata(name="initial", navigation=True)
    @property
    def initial(self) -> MultiTenantApplicationMetricsInitial:
        """Gets the initial property"""
        from office365.directory.multi_tenant_application_metrics_initial import (
            MultiTenantApplicationMetricsInitial,
        )

        return self.properties.get(
            "initial", MultiTenantApplicationMetricsInitial(self.context, ResourcePath("initial", self.resource_path))
        )

    @odata(name="recent", navigation=True)
    @property
    def recent(self) -> MultiTenantApplicationMetricsRecent:
        """Gets the recent property"""
        from office365.directory.multi_tenant_application_metrics_recent import (
            MultiTenantApplicationMetricsRecent,
        )

        return self.properties.get(
            "recent", MultiTenantApplicationMetricsRecent(self.context, ResourcePath("recent", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantApplicationMetrics"
