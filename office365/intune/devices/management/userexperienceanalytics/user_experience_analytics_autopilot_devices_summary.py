from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserExperienceAnalyticsAutopilotDevicesSummary(ClientValue):
    devicesNotAutopilotRegistered: int | None = None
    devicesWithoutAutopilotProfileAssigned: int | None = None
    totalWindows10DevicesWithoutTenantAttached: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAutopilotDevicesSummary"
