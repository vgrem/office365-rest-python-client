from __future__ import annotations

from office365.runtime.client_value import ClientValue


class UserExperienceAnalyticsAnomalySeverityOverview(ClientValue):
    highSeverityAnomalyCount: int | None = None
    informationalSeverityAnomalyCount: int | None = None
    lowSeverityAnomalyCount: int | None = None
    mediumSeverityAnomalyCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalySeverityOverview"
