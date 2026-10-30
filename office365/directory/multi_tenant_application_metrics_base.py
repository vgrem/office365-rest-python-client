from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class MultiTenantApplicationMetricsBase(Entity):
    @odata(name="inboundMonthlyTotalApplications")
    @property
    def inbound_monthly_total_applications(self) -> Optional[float]:
        """Gets the inboundMonthlyTotalApplications property"""
        return self.properties.get("inboundMonthlyTotalApplications", None)

    @odata(name="outboundMonthlyTotalApplications")
    @property
    def outbound_monthly_total_applications(self) -> Optional[float]:
        """Gets the outboundMonthlyTotalApplications property"""
        return self.properties.get("outboundMonthlyTotalApplications", None)

    @odata(name="watermarkDateTime")
    @property
    def watermark_date_time(self) -> Optional[datetime]:
        """Gets the watermarkDateTime property"""
        return self.properties.get("watermarkDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantApplicationMetricsBase"
