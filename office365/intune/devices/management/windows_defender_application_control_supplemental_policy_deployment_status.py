from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_statuses import (
    WindowsDefenderApplicationControlSupplementalPolicyStatuses,
)
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.windows_defender_application_control_supplemental_policy import (
        WindowsDefenderApplicationControlSupplementalPolicy,
    )


@version("beta")
class WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="lastSyncDateTime")
    @property
    def last_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastSyncDateTime property"""
        return self.properties.get("lastSyncDateTime", None)

    @odata(name="osDescription")
    @property
    def os_description(self) -> Optional[str]:
        """Gets the osDescription property"""
        return self.properties.get("osDescription", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="policyVersion")
    @property
    def policy_version(self) -> Optional[str]:
        """Gets the policyVersion property"""
        return self.properties.get("policyVersion", None)

    @odata(name="userName")
    @property
    def user_name(self) -> Optional[str]:
        """Gets the userName property"""
        return self.properties.get("userName", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @odata(name="policy", navigation=True)
    @property
    def policy(self) -> WindowsDefenderApplicationControlSupplementalPolicy:
        """Gets the policy property"""
        from office365.intune.devices.management.windows_defender_application_control_supplemental_policy import (
            WindowsDefenderApplicationControlSupplementalPolicy,
        )

        return self.properties.get(
            "policy",
            WindowsDefenderApplicationControlSupplementalPolicy(
                self.context, ResourcePath("policy", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus"

    @odata(name="deploymentStatus")
    @property
    def deployment_status(self) -> Optional[WindowsDefenderApplicationControlSupplementalPolicyStatuses]:
        """Gets the deploymentStatus property"""
        return self.properties.get("deploymentStatus", None)
