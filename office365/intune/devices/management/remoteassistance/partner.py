from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.devices.management.remoteassistance.onboardingstatus import RemoteAssistanceOnboardingStatus
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb


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

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    def begin_onboarding(self) -> Self:
        """beginOnboarding operation."""
        qry = ServiceOperationQuery(self, "beginOnboarding", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementServiceConfig.ReadWrite.All"],
        application=["DeviceManagementServiceConfig.ReadWrite.All"],
    )
    def disconnect(self) -> Self:
        """disconnect operation."""
        qry = ServiceOperationQuery(self, "disconnect", None, {}, None, None)
        self.context.add_query(qry)
        return self
