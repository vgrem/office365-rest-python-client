from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsDeviceStartupProcessPerformance(Entity):
    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @odata(name="medianImpactInMs")
    @property
    def median_impact_in_ms(self) -> Optional[int]:
        """Gets the medianImpactInMs property"""
        return self.properties.get("medianImpactInMs", None)

    @odata(name="processName")
    @property
    def process_name(self) -> Optional[str]:
        """Gets the processName property"""
        return self.properties.get("processName", None)

    @odata(name="productName")
    @property
    def product_name(self) -> Optional[str]:
        """Gets the productName property"""
        return self.properties.get("productName", None)

    @odata(name="publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @odata(name="totalImpactInMs")
    @property
    def total_impact_in_ms(self) -> Optional[int]:
        """Gets the totalImpactInMs property"""
        return self.properties.get("totalImpactInMs", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceStartupProcessPerformance"
