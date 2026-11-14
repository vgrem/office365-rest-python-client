from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.common.managed_app_device_threat_level import ManagedAppDeviceThreatLevel
from office365.common.managed_app_remediation_action import ManagedAppRemediationAction
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.app.protections.windows_managed_app_clipboard_sharing_level import (
    WindowsManagedAppClipboardSharingLevel,
)
from office365.intune.devices.management.managed.app.protections.windows_managed_app_data_transfer_level import (
    WindowsManagedAppDataTransferLevel,
)
from office365.intune.devices.management.managed.app.protections.windows_managed_app_data_transfer_locations import (
    WindowsManagedAppDataTransferLocations,
)
from office365.intune.policies.managed_app import ManagedAppPolicy
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from datetime import timedelta

    from office365.intune.devices.management.managed.app.mobile.app import ManagedMobileApp
    from office365.intune.devices.management.managed.app.policy_deployment_summary import (
        ManagedAppPolicyDeploymentSummary,
    )
    from office365.intune.devices.management.managed.app.protections.targeted_managed_app_policy_assignment import (
        TargetedManagedAppPolicyAssignment,
    )


@version("beta")
class WindowsManagedAppProtection(ManagedAppPolicy):
    @odata(name="deployedAppCount")
    @property
    def deployed_app_count(self) -> Optional[int]:
        """Gets the deployedAppCount property"""
        return self.properties.get("deployedAppCount", None)

    @odata(name="isAssigned")
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @odata(name="maximumRequiredOsVersion")
    @property
    def maximum_required_os_version(self) -> Optional[str]:
        """Gets the maximumRequiredOsVersion property"""
        return self.properties.get("maximumRequiredOsVersion", None)

    @odata(name="maximumWarningOsVersion")
    @property
    def maximum_warning_os_version(self) -> Optional[str]:
        """Gets the maximumWarningOsVersion property"""
        return self.properties.get("maximumWarningOsVersion", None)

    @odata(name="maximumWipeOsVersion")
    @property
    def maximum_wipe_os_version(self) -> Optional[str]:
        """Gets the maximumWipeOsVersion property"""
        return self.properties.get("maximumWipeOsVersion", None)

    @odata(name="minimumRequiredAppVersion")
    @property
    def minimum_required_app_version(self) -> Optional[str]:
        """Gets the minimumRequiredAppVersion property"""
        return self.properties.get("minimumRequiredAppVersion", None)

    @odata(name="minimumRequiredOsVersion")
    @property
    def minimum_required_os_version(self) -> Optional[str]:
        """Gets the minimumRequiredOsVersion property"""
        return self.properties.get("minimumRequiredOsVersion", None)

    @odata(name="minimumRequiredSdkVersion")
    @property
    def minimum_required_sdk_version(self) -> Optional[str]:
        """Gets the minimumRequiredSdkVersion property"""
        return self.properties.get("minimumRequiredSdkVersion", None)

    @odata(name="minimumWarningAppVersion")
    @property
    def minimum_warning_app_version(self) -> Optional[str]:
        """Gets the minimumWarningAppVersion property"""
        return self.properties.get("minimumWarningAppVersion", None)

    @odata(name="minimumWarningOsVersion")
    @property
    def minimum_warning_os_version(self) -> Optional[str]:
        """Gets the minimumWarningOsVersion property"""
        return self.properties.get("minimumWarningOsVersion", None)

    @odata(name="minimumWipeAppVersion")
    @property
    def minimum_wipe_app_version(self) -> Optional[str]:
        """Gets the minimumWipeAppVersion property"""
        return self.properties.get("minimumWipeAppVersion", None)

    @odata(name="minimumWipeOsVersion")
    @property
    def minimum_wipe_os_version(self) -> Optional[str]:
        """Gets the minimumWipeOsVersion property"""
        return self.properties.get("minimumWipeOsVersion", None)

    @odata(name="minimumWipeSdkVersion")
    @property
    def minimum_wipe_sdk_version(self) -> Optional[str]:
        """Gets the minimumWipeSdkVersion property"""
        return self.properties.get("minimumWipeSdkVersion", None)

    @odata(name="periodOfflineBeforeAccessCheck")
    @property
    def period_offline_before_access_check(self) -> Optional[timedelta]:
        """Gets the periodOfflineBeforeAccessCheck property"""
        return self.properties.get("periodOfflineBeforeAccessCheck", None)

    @odata(name="periodOfflineBeforeWipeIsEnforced")
    @property
    def period_offline_before_wipe_is_enforced(self) -> Optional[timedelta]:
        """Gets the periodOfflineBeforeWipeIsEnforced property"""
        return self.properties.get("periodOfflineBeforeWipeIsEnforced", None)

    @odata(name="printBlocked")
    @property
    def print_blocked(self) -> Optional[bool]:
        """Gets the printBlocked property"""
        return self.properties.get("printBlocked", None)

    @odata(name="apps", navigation=True)
    @property
    def apps(self) -> EntityCollection[ManagedMobileApp]:
        """Gets the apps property"""
        from office365.intune.devices.management.managed.app.mobile.app import ManagedMobileApp

        return self.properties.get(
            "apps",
            EntityCollection[ManagedMobileApp](self.context, ManagedMobileApp, ResourcePath("apps", self.resource_path)),
        )

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[TargetedManagedAppPolicyAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.managed.app.protections.targeted_managed_app_policy_assignment import (
            TargetedManagedAppPolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[TargetedManagedAppPolicyAssignment](
                self.context, TargetedManagedAppPolicyAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="deploymentSummary", navigation=True)
    @property
    def deployment_summary(self) -> ManagedAppPolicyDeploymentSummary:
        """Gets the deploymentSummary property"""
        from office365.intune.devices.management.managed.app.policy_deployment_summary import (
            ManagedAppPolicyDeploymentSummary,
        )

        return self.properties.get(
            "deploymentSummary",
            ManagedAppPolicyDeploymentSummary(self.context, ResourcePath("deploymentSummary", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagedAppProtection"

    @require_permission(
        delegated=[
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.ReadWrite.All",
        ],
        application=[
            "DeviceManagementConfiguration.ReadWrite.All",
            "DeviceManagementApps.ReadWrite.All",
        ],
    )
    def assign(self, assignments: ClientValueCollection[TargetedManagedAppPolicyAssignment]) -> Self:
        """assign operation.

        Args:
            assignments (ClientValueCollection[TargetedManagedAppPolicyAssignment]):
                assignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="allowedInboundDataTransferSourceApps")
    @property
    def allowed_inbound_data_transfer_source_apps(self) -> Optional[WindowsManagedAppDataTransferLocations]:
        """Gets the allowedInboundDataTransferSourceApps property"""
        return self.properties.get("allowedInboundDataTransferSourceApps", None)

    @odata(name="allowedInboundDataTransferSources")
    @property
    def allowed_inbound_data_transfer_sources(self) -> Optional[WindowsManagedAppDataTransferLevel]:
        """Gets the allowedInboundDataTransferSources property"""
        return self.properties.get("allowedInboundDataTransferSources", None)

    @odata(name="allowedOutboundClipboardSharingLevel")
    @property
    def allowed_outbound_clipboard_sharing_level(self) -> Optional[WindowsManagedAppClipboardSharingLevel]:
        """Gets the allowedOutboundClipboardSharingLevel property"""
        return self.properties.get("allowedOutboundClipboardSharingLevel", None)

    @odata(name="allowedOutboundDataTransferDestinationApps")
    @property
    def allowed_outbound_data_transfer_destination_apps(self) -> Optional[WindowsManagedAppDataTransferLocations]:
        """Gets the allowedOutboundDataTransferDestinationApps property"""
        return self.properties.get("allowedOutboundDataTransferDestinationApps", None)

    @odata(name="allowedOutboundDataTransferDestinations")
    @property
    def allowed_outbound_data_transfer_destinations(self) -> Optional[WindowsManagedAppDataTransferLevel]:
        """Gets the allowedOutboundDataTransferDestinations property"""
        return self.properties.get("allowedOutboundDataTransferDestinations", None)

    @odata(name="appActionIfUnableToAuthenticateUser")
    @property
    def app_action_if_unable_to_authenticate_user(self) -> Optional[ManagedAppRemediationAction]:
        """Gets the appActionIfUnableToAuthenticateUser property"""
        return self.properties.get("appActionIfUnableToAuthenticateUser", None)

    @odata(name="maximumAllowedDeviceThreatLevel")
    @property
    def maximum_allowed_device_threat_level(self) -> Optional[ManagedAppDeviceThreatLevel]:
        """Gets the maximumAllowedDeviceThreatLevel property"""
        return self.properties.get("maximumAllowedDeviceThreatLevel", None)

    @odata(name="mobileThreatDefenseRemediationAction")
    @property
    def mobile_threat_defense_remediation_action(self) -> Optional[ManagedAppRemediationAction]:
        """Gets the mobileThreatDefenseRemediationAction property"""
        return self.properties.get("mobileThreatDefenseRemediationAction", None)
