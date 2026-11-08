from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management_configuration_platforms import DeviceManagementConfigurationPlatforms
from office365.intune.devices.management_configuration_technologies import DeviceManagementConfigurationTechnologies
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_compliance_scheduled_action_for_rule import (
        DeviceManagementComplianceScheduledActionForRule,
    )
    from office365.intune.devices.management_configuration_policy_assignment import (
        DeviceManagementConfigurationPolicyAssignment,
    )
    from office365.intune.devices.management_configuration_setting import DeviceManagementConfigurationSetting


@version("beta")
class DeviceManagementCompliancePolicy(Entity):
    @odata(name="createdDateTime", readonly=True)
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

    @odata(name="isAssigned", readonly=True)
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @odata(name="lastModifiedDateTime", readonly=True)
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

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="settingCount", readonly=True)
    @property
    def setting_count(self) -> Optional[int]:
        """Gets the settingCount property"""
        return self.properties.get("settingCount", None)

    @odata(name="technologies")
    @property
    def technologies(self) -> Optional[DeviceManagementConfigurationTechnologies]:
        """Gets the technologies property"""
        return self.properties.get("technologies", None)

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

    @odata(name="scheduledActionsForRule", navigation=True)
    @property
    def scheduled_actions_for_rule(self) -> EntityCollection[DeviceManagementComplianceScheduledActionForRule]:
        """Gets the scheduledActionsForRule property"""
        from office365.intune.devices.management_compliance_scheduled_action_for_rule import (
            DeviceManagementComplianceScheduledActionForRule,
        )

        return self.properties.get(
            "scheduledActionsForRule",
            EntityCollection[DeviceManagementComplianceScheduledActionForRule](
                self.context,
                DeviceManagementComplianceScheduledActionForRule,
                ResourcePath("scheduledActionsForRule", self.resource_path),
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
        return "microsoft.graph.DeviceManagementCompliancePolicy"

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

    def set_scheduled_actions(
        self, scheduled_actions: ClientValueCollection[DeviceManagementComplianceScheduledActionForRule]
    ) -> EntityCollection[DeviceManagementComplianceScheduledActionForRule]:
        """setScheduledActions operation.

        Args:
            scheduled_actions (ClientValueCollection[DeviceManagementComplianceScheduledActionForRule]):
                scheduledActions parameter
        """
        from office365.intune.devices.management_compliance_scheduled_action_for_rule import (
            DeviceManagementComplianceScheduledActionForRule,
        )

        return_type = EntityCollection(self.context, DeviceManagementComplianceScheduledActionForRule)
        qry = ServiceOperationQuery(
            self, "setScheduledActions", None, {"scheduledActions": scheduled_actions}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
