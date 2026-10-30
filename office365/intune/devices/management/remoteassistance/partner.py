from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.remoteassistance.onboardingstatus import RemoteAssistanceOnboardingStatus
from office365.runtime.types.odata_property import odata


class RemoteAssistancePartner(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastConnectionDateTime")
    @property
    def last_connection_date_time(self) -> Optional[datetime]:
        """Gets the lastConnectionDateTime property"""
        return self.properties.get("lastConnectionDateTime", datetime.min)

    @odata(name="onboardingStatus")
    @property
    def onboarding_status(self) -> RemoteAssistanceOnboardingStatus:
        """Gets the onboardingStatus property"""
        return self.properties.get("onboardingStatus", RemoteAssistanceOnboardingStatus.notOnboarded)

    @odata(name="onboardingUrl")
    @property
    def onboarding_url(self) -> Optional[str]:
        """Gets the onboardingUrl property"""
        return self.properties.get("onboardingUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RemoteAssistancePartner"
