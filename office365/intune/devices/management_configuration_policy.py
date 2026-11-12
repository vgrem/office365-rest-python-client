from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management_configuration_platforms import DeviceManagementConfigurationPlatforms
from office365.intune.devices.management_configuration_policy_template_reference import (
    DeviceManagementConfigurationPolicyTemplateReference,
)
from office365.intune.devices.management_configuration_technologies import DeviceManagementConfigurationTechnologies
from office365.intune.devices.management_priority_meta_data import DeviceManagementPriorityMetaData
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy
    from office365.intune.devices.management_configuration_policy_assignment import (
        DeviceManagementConfigurationPolicyAssignment,
    )
    from office365.intune.devices.management_configuration_setting import DeviceManagementConfigurationSetting


@version("beta")
class DeviceManagementConfigurationPolicy(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="creationSource")
    @property
    def creation_source(self) -> Optional[str]:
        """Gets the creationSource property"""
        return self.properties.get("creationSource", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="disableEntraGroupPolicyAssignment")
    @property
    def disable_entra_group_policy_assignment(self) -> Optional[bool]:
        """Gets the disableEntraGroupPolicyAssignment property"""
        return self.properties.get("disableEntraGroupPolicyAssignment", None)

    @odata(name="isAssigned", readonly=True)
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="platforms")
    @property
    def platforms(self) -> Optional[DeviceManagementConfigurationPlatforms]:
        """Gets the platforms property"""
        return self.properties.get("platforms", None)

    @odata(name="priorityMetaData")
    @property
    def priority_meta_data(self) -> Optional[DeviceManagementPriorityMetaData]:
        """Gets the priorityMetaData property"""
        return self.properties.get("priorityMetaData", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="settingCount")
    @property
    def setting_count(self) -> Optional[int]:
        """Gets the settingCount property"""
        return self.properties.get("settingCount", None)

    @odata(name="technologies")
    @property
    def technologies(self) -> Optional[DeviceManagementConfigurationTechnologies]:
        """Gets the technologies property"""
        return self.properties.get("technologies", None)

    @odata(name="templateReference")
    @property
    def template_reference(self) -> Optional[DeviceManagementConfigurationPolicyTemplateReference]:
        """Gets the templateReference property"""
        return self.properties.get("templateReference", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[DeviceManagementConfigurationPolicyAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management_configuration_policy_assignment import (
            DeviceManagementConfigurationPolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[DeviceManagementConfigurationPolicyAssignment](
                self.context,
                DeviceManagementConfigurationPolicyAssignment,
                ResourcePath("assignments", self.resource_path),
            ),
        )

    @odata(name="settings", navigation=True)
    @property
    def settings(self) -> EntityCollection[DeviceManagementConfigurationSetting]:
        """Gets the settings property"""
        from office365.intune.devices.management_configuration_setting import DeviceManagementConfigurationSetting

        return self.properties.get(
            "settings",
            EntityCollection[DeviceManagementConfigurationSetting](
                self.context, DeviceManagementConfigurationSetting, ResourcePath("settings", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationPolicy"

    @verb(role="action", effect="write")
    def assign(
        self, assignments: ClientValueCollection[DeviceManagementConfigurationPolicyAssignment]
    ) -> EntityCollection[DeviceManagementConfigurationPolicyAssignment]:
        """assign operation.

        Args:
            assignments (ClientValueCollection[DeviceManagementConfigurationPolicyAssignment]):
                assignments parameter
        """
        from office365.intune.devices.management_configuration_policy_assignment import (
            DeviceManagementConfigurationPolicyAssignment,
        )

        return_type = EntityCollection(self.context, DeviceManagementConfigurationPolicyAssignment)
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementConfiguration.Read.All"],
        application=["DeviceManagementConfiguration.Read.All"],
    )
    def clear_enrollment_time_device_membership_target(self) -> ClientResult[bool]:
        """clearEnrollmentTimeDeviceMembershipTarget operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "clearEnrollmentTimeDeviceMembershipTarget", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def create_copy(self, display_name: str, description: str) -> DeviceManagementConfigurationPolicy:
        """createCopy operation.

        Args:
            display_name (str):
                displayName parameter
            description (str):
                description parameter
        """
        from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy

        return_type = DeviceManagementConfigurationPolicy(self.context)
        qry = ServiceOperationQuery(
            self, "createCopy", None, {"displayName": display_name, "description": description}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def reorder(self, priority: int) -> Self:
        """reorder operation.

        Args:
            priority (int):
                priority parameter
        """
        qry = ServiceOperationQuery(self, "reorder", None, {"priority": priority}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All"],
    )
    def retrieve_latest_upgrade_default_baseline_policy(self) -> DeviceManagementConfigurationPolicy:
        """retrieveLatestUpgradeDefaultBaselinePolicy operation."""
        from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy

        return_type = DeviceManagementConfigurationPolicy(self.context)
        qry = FunctionQuery(self, "retrieveLatestUpgradeDefaultBaselinePolicy", None, return_type)
        self.context.add_query(qry)
        return return_type
