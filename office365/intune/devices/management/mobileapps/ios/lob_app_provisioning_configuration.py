from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission, requires_license
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.app.mobile.configuration_device_status import (
        ManagedDeviceMobileAppConfigurationDeviceStatus,
    )
    from office365.intune.devices.management.managed.app.mobile.configuration_user_status import (
        ManagedDeviceMobileAppConfigurationUserStatus,
    )
    from office365.intune.devices.management.mobileapps.ios.lob_app_provisioning_configuration_assignment import (
        IosLobAppProvisioningConfigurationAssignment,
    )
    from office365.intune.devices.management.mobileapps.ios.mobile_app_provisioning_config_group_assignment import (
        MobileAppProvisioningConfigGroupAssignment,
    )


@version("beta")
@requires_license("INTUNE_A")
class IosLobAppProvisioningConfiguration(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="payload")
    @property
    def payload(self) -> Optional[bytes]:
        """Gets the payload property"""
        return self.properties.get("payload", None)

    @odata(name="payloadFileName")
    @property
    def payload_file_name(self) -> Optional[str]:
        """Gets the payloadFileName property"""
        return self.properties.get("payloadFileName", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[IosLobAppProvisioningConfigurationAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.mobileapps.ios.lob_app_provisioning_configuration_assignment import (
            IosLobAppProvisioningConfigurationAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[IosLobAppProvisioningConfigurationAssignment](
                self.context,
                IosLobAppProvisioningConfigurationAssignment,
                ResourcePath("assignments", self.resource_path),
            ),
        )

    @odata(name="deviceStatuses", navigation=True)
    @property
    def device_statuses(self) -> EntityCollection[ManagedDeviceMobileAppConfigurationDeviceStatus]:
        """Gets the deviceStatuses property"""
        from office365.intune.devices.management.managed.app.mobile.configuration_device_status import (
            ManagedDeviceMobileAppConfigurationDeviceStatus,
        )

        return self.properties.get(
            "deviceStatuses",
            EntityCollection[ManagedDeviceMobileAppConfigurationDeviceStatus](
                self.context,
                ManagedDeviceMobileAppConfigurationDeviceStatus,
                ResourcePath("deviceStatuses", self.resource_path),
            ),
        )

    @odata(name="groupAssignments", navigation=True)
    @property
    def group_assignments(self) -> EntityCollection[MobileAppProvisioningConfigGroupAssignment]:
        """Gets the groupAssignments property"""
        from office365.intune.devices.management.mobileapps.ios.mobile_app_provisioning_config_group_assignment import (
            MobileAppProvisioningConfigGroupAssignment,
        )

        return self.properties.get(
            "groupAssignments",
            EntityCollection[MobileAppProvisioningConfigGroupAssignment](
                self.context,
                MobileAppProvisioningConfigGroupAssignment,
                ResourcePath("groupAssignments", self.resource_path),
            ),
        )

    @odata(name="userStatuses", navigation=True)
    @property
    def user_statuses(self) -> EntityCollection[ManagedDeviceMobileAppConfigurationUserStatus]:
        """Gets the userStatuses property"""
        from office365.intune.devices.management.managed.app.mobile.configuration_user_status import (
            ManagedDeviceMobileAppConfigurationUserStatus,
        )

        return self.properties.get(
            "userStatuses",
            EntityCollection[ManagedDeviceMobileAppConfigurationUserStatus](
                self.context,
                ManagedDeviceMobileAppConfigurationUserStatus,
                ResourcePath("userStatuses", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosLobAppProvisioningConfiguration"

    @require_permission(
        delegated=[
            "DeviceManagementApps.ReadWrite.All",
        ],
        application=[
            "DeviceManagementApps.ReadWrite.All",
        ],
    )
    def assign(
        self,
        app_provisioning_configuration_group_assignments: ClientValueCollection[
            MobileAppProvisioningConfigGroupAssignment
        ],
        ios_lob_app_provisioning_config_assignments: ClientValueCollection[IosLobAppProvisioningConfigurationAssignment],
    ) -> Self:
        """assign operation.

        Args:
            app_provisioning_configuration_group_assignments:
                appProvisioningConfigurationGroupAssignments parameter
            ios_lob_app_provisioning_config_assignments:
                iOSLobAppProvisioningConfigAssignments parameter
        """
        qry = ServiceOperationQuery(
            self,
            "assign",
            None,
            {
                "appProvisioningConfigurationGroupAssignments": app_provisioning_configuration_group_assignments,
                "iOSLobAppProvisioningConfigAssignments": ios_lob_app_provisioning_config_assignments,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self
