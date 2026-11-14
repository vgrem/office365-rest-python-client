from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthRuntimeDetails(Entity):
    @odata(name="activeDevices")
    @property
    def active_devices(self) -> Optional[int]:
        """Gets the activeDevices property"""
        return self.properties.get("activeDevices", None)

    @odata(name="batteryRuntimeFair")
    @property
    def battery_runtime_fair(self) -> Optional[int]:
        """Gets the batteryRuntimeFair property"""
        return self.properties.get("batteryRuntimeFair", None)

    @odata(name="batteryRuntimeGood")
    @property
    def battery_runtime_good(self) -> Optional[int]:
        """Gets the batteryRuntimeGood property"""
        return self.properties.get("batteryRuntimeGood", None)

    @odata(name="batteryRuntimePoor")
    @property
    def battery_runtime_poor(self) -> Optional[int]:
        """Gets the batteryRuntimePoor property"""
        return self.properties.get("batteryRuntimePoor", None)

    @odata(name="lastRefreshedDateTime")
    @property
    def last_refreshed_date_time(self) -> Optional[datetime]:
        """Gets the lastRefreshedDateTime property"""
        return self.properties.get("lastRefreshedDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthRuntimeDetails"
