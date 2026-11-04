from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class B2BSignInActivityMetricsBase(Entity):
    @odata(name="inboundMonthlyTotalApplications")
    @property
    def inbound_monthly_total_applications(self) -> Optional[float]:
        """Gets the inboundMonthlyTotalApplications property"""
        return self.properties.get("inboundMonthlyTotalApplications", None)

    @odata(name="inboundMonthlyTotalUsers")
    @property
    def inbound_monthly_total_users(self) -> Optional[float]:
        """Gets the inboundMonthlyTotalUsers property"""
        return self.properties.get("inboundMonthlyTotalUsers", None)

    @odata(name="outboundMonthlyTotalApplications")
    @property
    def outbound_monthly_total_applications(self) -> Optional[float]:
        """Gets the outboundMonthlyTotalApplications property"""
        return self.properties.get("outboundMonthlyTotalApplications", None)

    @odata(name="outboundMonthlyTotalUsers")
    @property
    def outbound_monthly_total_users(self) -> Optional[float]:
        """Gets the outboundMonthlyTotalUsers property"""
        return self.properties.get("outboundMonthlyTotalUsers", None)

    @odata(name="watermarkDateTime")
    @property
    def watermark_date_time(self) -> Optional[datetime]:
        """Gets the watermarkDateTime property"""
        return self.properties.get("watermarkDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.B2BSignInActivityMetricsBase"
