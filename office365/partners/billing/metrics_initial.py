from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.partners.billing.metrics_base import BillingMetricsBase
from office365.runtime.types.odata_property import odata


class BillingMetricsInitial(BillingMetricsBase):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BillingMetricsInitial"
