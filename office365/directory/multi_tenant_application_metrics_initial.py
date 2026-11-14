from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.multi_tenant_application_metrics_base import MultiTenantApplicationMetricsBase
from office365.runtime.types.odata_property import odata


class MultiTenantApplicationMetricsInitial(MultiTenantApplicationMetricsBase):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantApplicationMetricsInitial"
