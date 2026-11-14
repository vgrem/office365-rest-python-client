from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.partners.billing.metrics_base import BillingMetricsBase
from office365.runtime.types.odata_property import odata


class BillingMetricsRecent(BillingMetricsBase):
    @odata(name="updateDateTime")
    @property
    def update_date_time(self) -> Optional[datetime]:
        """Gets the updateDateTime property"""
        return self.properties.get("updateDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BillingMetricsRecent"
