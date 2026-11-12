from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management_configuration_setting_instance import (
    DeviceManagementConfigurationSettingInstance,
)
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy
    from office365.intune.devices.management_reusable_policy_setting import DeviceManagementReusablePolicySetting


@version("beta")
class DeviceManagementReusablePolicySetting(Entity):
    @odata(name="createdDateTime", readonly=True)
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

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="referencingConfigurationPolicyCount", readonly=True)
    @property
    def referencing_configuration_policy_count(self) -> Optional[int]:
        """Gets the referencingConfigurationPolicyCount property"""
        return self.properties.get("referencingConfigurationPolicyCount", None)

    @odata(name="settingDefinitionId")
    @property
    def setting_definition_id(self) -> Optional[str]:
        """Gets the settingDefinitionId property"""
        return self.properties.get("settingDefinitionId", None)

    @odata(name="settingInstance")
    @property
    def setting_instance(self) -> Optional[DeviceManagementConfigurationSettingInstance]:
        """Gets the settingInstance property"""
        return self.properties.get("settingInstance", None)

    @odata(name="version", readonly=True)
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="referencingConfigurationPolicies", navigation=True)
    @property
    def referencing_configuration_policies(self) -> EntityCollection[DeviceManagementConfigurationPolicy]:
        """Gets the referencingConfigurationPolicies property"""
        from office365.intune.devices.management_configuration_policy import DeviceManagementConfigurationPolicy

        return self.properties.get(
            "referencingConfigurationPolicies",
            EntityCollection[DeviceManagementConfigurationPolicy](
                self.context,
                DeviceManagementConfigurationPolicy,
                ResourcePath("referencingConfigurationPolicies", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementReusablePolicySetting"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def clone(self) -> DeviceManagementReusablePolicySetting:
        """clone operation."""
        from office365.intune.devices.management_reusable_policy_setting import DeviceManagementReusablePolicySetting

        return_type = DeviceManagementReusablePolicySetting(self.context)
        qry = ServiceOperationQuery(self, "clone", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
