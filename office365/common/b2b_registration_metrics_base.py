from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class B2BRegistrationMetricsBase(Entity):
    @odata(name="inboundTotalUsers")
    @property
    def inbound_total_users(self) -> Optional[float]:
        """Gets the inboundTotalUsers property"""
        return self.properties.get("inboundTotalUsers", None)

    @odata(name="outboundTotalUsers")
    @property
    def outbound_total_users(self) -> Optional[float]:
        """Gets the outboundTotalUsers property"""
        return self.properties.get("outboundTotalUsers", None)

    @odata(name="watermarkDateTime")
    @property
    def watermark_date_time(self) -> Optional[datetime]:
        """Gets the watermarkDateTime property"""
        return self.properties.get("watermarkDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.B2BRegistrationMetricsBase"
