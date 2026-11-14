from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsImpactingProcess(Entity):
    @odata(name="category")
    @property
    def category(self) -> Optional[str]:
        """Gets the category property"""
        return self.properties.get("category", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="impactValue")
    @property
    def impact_value(self) -> Optional[float]:
        """Gets the impactValue property"""
        return self.properties.get("impactValue", None)

    @odata(name="processName")
    @property
    def process_name(self) -> Optional[str]:
        """Gets the processName property"""
        return self.properties.get("processName", None)

    @odata(name="publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsImpactingProcess"
