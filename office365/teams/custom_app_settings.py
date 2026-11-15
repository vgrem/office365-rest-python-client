from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.teams.apps.development_platforms import AppDevelopmentPlatforms


class CustomAppSettings(ClientValue):
    developerToolsForShowingAppUsageMetrics: AppDevelopmentPlatforms = AppDevelopmentPlatforms.developerPortal

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomAppSettings"
