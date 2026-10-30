from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsDeviceStartupProcess(Entity):
    @odata(name="managedDeviceId")
    @property
    def managed_device_id(self) -> Optional[str]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

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

    @odata(name="startupImpactInMs")
    @property
    def startup_impact_in_ms(self) -> Optional[int]:
        """Gets the startupImpactInMs property"""
        return self.properties.get("startupImpactInMs", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceStartupProcess"
