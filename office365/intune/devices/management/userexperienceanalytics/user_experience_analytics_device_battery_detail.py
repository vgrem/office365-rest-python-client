from __future__ import annotations

from office365.runtime.client_value import ClientValue


class UserExperienceAnalyticsDeviceBatteryDetail(ClientValue):
    batteryId: str | None = None
    fullBatteryDrainCount: int | None = None
    maxCapacityPercentage: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceBatteryDetail"
