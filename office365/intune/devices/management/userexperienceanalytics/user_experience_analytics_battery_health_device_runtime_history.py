from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="estimatedRuntimeInMinutes")
    @property
    def estimated_runtime_in_minutes(self) -> Optional[int]:
        """Gets the estimatedRuntimeInMinutes property"""
        return self.properties.get("estimatedRuntimeInMinutes", None)

    @odata(name="runtimeDateTime")
    @property
    def runtime_date_time(self) -> Optional[str]:
        """Gets the runtimeDateTime property"""
        return self.properties.get("runtimeDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthDeviceRuntimeHistory"
