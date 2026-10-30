from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.mobileapps.managed.app_policy_deployment_summary_per_app import (
        ManagedAppPolicyDeploymentSummaryPerApp,
    )


class ManagedAppPolicyDeploymentSummary(Entity):
    @odata(name="configurationDeployedUserCount")
    @property
    def configuration_deployed_user_count(self) -> Optional[int]:
        """Gets the configurationDeployedUserCount property"""
        return self.properties.get("configurationDeployedUserCount", None)

    @odata(name="configurationDeploymentSummaryPerApp")
    @property
    def configuration_deployment_summary_per_app(self) -> ClientValueCollection[ManagedAppPolicyDeploymentSummaryPerApp]:
        """Gets the configurationDeploymentSummaryPerApp property"""
        from office365.intune.devices.management.mobileapps.managed.app_policy_deployment_summary_per_app import (
            ManagedAppPolicyDeploymentSummaryPerApp,
        )

        return self.properties.get(
            "configurationDeploymentSummaryPerApp",
            ClientValueCollection[ManagedAppPolicyDeploymentSummaryPerApp](ManagedAppPolicyDeploymentSummaryPerApp),
        )

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastRefreshTime")
    @property
    def last_refresh_time(self) -> Optional[datetime]:
        """Gets the lastRefreshTime property"""
        return self.properties.get("lastRefreshTime", datetime.min)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAppPolicyDeploymentSummary"
