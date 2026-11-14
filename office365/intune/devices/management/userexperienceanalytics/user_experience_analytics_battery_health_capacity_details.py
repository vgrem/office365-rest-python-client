from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthCapacityDetails(Entity):
    @odata(name="activeDevices")
    @property
    def active_devices(self) -> Optional[int]:
        """Gets the activeDevices property"""
        return self.properties.get("activeDevices", None)

    @odata(name="batteryCapacityFair")
    @property
    def battery_capacity_fair(self) -> Optional[int]:
        """Gets the batteryCapacityFair property"""
        return self.properties.get("batteryCapacityFair", None)

    @odata(name="batteryCapacityGood")
    @property
    def battery_capacity_good(self) -> Optional[int]:
        """Gets the batteryCapacityGood property"""
        return self.properties.get("batteryCapacityGood", None)

    @odata(name="batteryCapacityPoor")
    @property
    def battery_capacity_poor(self) -> Optional[int]:
        """Gets the batteryCapacityPoor property"""
        return self.properties.get("batteryCapacityPoor", None)

    @odata(name="lastRefreshedDateTime")
    @property
    def last_refreshed_date_time(self) -> Optional[datetime]:
        """Gets the lastRefreshedDateTime property"""
        return self.properties.get("lastRefreshedDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthCapacityDetails"
