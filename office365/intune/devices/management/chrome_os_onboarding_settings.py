from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version
from office365.security.alerts.states.onboarding import OnboardingStatus


@version("beta")
class ChromeOSOnboardingSettings(Entity):
    @odata(name="lastDirectorySyncDateTime")
    @property
    def last_directory_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastDirectorySyncDateTime property"""
        return self.properties.get("lastDirectorySyncDateTime", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="onboardingStatus")
    @property
    def onboarding_status(self) -> OnboardingStatus:
        """Gets the onboardingStatus property"""
        return self.properties.get("onboardingStatus", OnboardingStatus.insufficientInfo)

    @odata(name="ownerUserPrincipalName")
    @property
    def owner_user_principal_name(self) -> Optional[str]:
        """Gets the ownerUserPrincipalName property"""
        return self.properties.get("ownerUserPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChromeOSOnboardingSettings"
