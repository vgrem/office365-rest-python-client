from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_intent import DeviceManagementIntent
    from office365.intune.devices.management_intent_assignment import DeviceManagementIntentAssignment
    from office365.intune.devices.management_intent_device_setting_state_summary import (
        DeviceManagementIntentDeviceSettingStateSummary,
    )
    from office365.intune.devices.management_intent_device_state import DeviceManagementIntentDeviceState
    from office365.intune.devices.management_intent_device_state_summary import DeviceManagementIntentDeviceStateSummary
    from office365.intune.devices.management_intent_setting_category import DeviceManagementIntentSettingCategory
    from office365.intune.devices.management_intent_user_state import DeviceManagementIntentUserState
    from office365.intune.devices.management_intent_user_state_summary import DeviceManagementIntentUserStateSummary
    from office365.intune.devices.management_setting_instance import DeviceManagementSettingInstance


@version("beta")
class DeviceManagementIntent(Entity):
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

    @odata(name="isAssigned")
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @odata(name="isMigratingToConfigurationPolicy")
    @property
    def is_migrating_to_configuration_policy(self) -> Optional[bool]:
        """Gets the isMigratingToConfigurationPolicy property"""
        return self.properties.get("isMigratingToConfigurationPolicy", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="templateId")
    @property
    def template_id(self) -> Optional[str]:
        """Gets the templateId property"""
        return self.properties.get("templateId", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[DeviceManagementIntentAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management_intent_assignment import DeviceManagementIntentAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[DeviceManagementIntentAssignment](
                self.context, DeviceManagementIntentAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="categories", navigation=True)
    @property
    def categories(self) -> EntityCollection[DeviceManagementIntentSettingCategory]:
        """Gets the categories property"""
        from office365.intune.devices.management_intent_setting_category import DeviceManagementIntentSettingCategory

        return self.properties.get(
            "categories",
            EntityCollection[DeviceManagementIntentSettingCategory](
                self.context, DeviceManagementIntentSettingCategory, ResourcePath("categories", self.resource_path)
            ),
        )

    @odata(name="deviceSettingStateSummaries", navigation=True)
    @property
    def device_setting_state_summaries(self) -> EntityCollection[DeviceManagementIntentDeviceSettingStateSummary]:
        """Gets the deviceSettingStateSummaries property"""
        from office365.intune.devices.management_intent_device_setting_state_summary import (
            DeviceManagementIntentDeviceSettingStateSummary,
        )

        return self.properties.get(
            "deviceSettingStateSummaries",
            EntityCollection[DeviceManagementIntentDeviceSettingStateSummary](
                self.context,
                DeviceManagementIntentDeviceSettingStateSummary,
                ResourcePath("deviceSettingStateSummaries", self.resource_path),
            ),
        )

    @odata(name="deviceStates", navigation=True)
    @property
    def device_states(self) -> EntityCollection[DeviceManagementIntentDeviceState]:
        """Gets the deviceStates property"""
        from office365.intune.devices.management_intent_device_state import DeviceManagementIntentDeviceState

        return self.properties.get(
            "deviceStates",
            EntityCollection[DeviceManagementIntentDeviceState](
                self.context, DeviceManagementIntentDeviceState, ResourcePath("deviceStates", self.resource_path)
            ),
        )

    @odata(name="deviceStateSummary", navigation=True)
    @property
    def device_state_summary(self) -> DeviceManagementIntentDeviceStateSummary:
        """Gets the deviceStateSummary property"""
        from office365.intune.devices.management_intent_device_state_summary import (
            DeviceManagementIntentDeviceStateSummary,
        )

        return self.properties.get(
            "deviceStateSummary",
            DeviceManagementIntentDeviceStateSummary(
                self.context, ResourcePath("deviceStateSummary", self.resource_path)
            ),
        )

    @odata(name="settings", navigation=True)
    @property
    def settings(self) -> EntityCollection[DeviceManagementSettingInstance]:
        """Gets the settings property"""
        from office365.intune.devices.management_setting_instance import DeviceManagementSettingInstance

        return self.properties.get(
            "settings",
            EntityCollection[DeviceManagementSettingInstance](
                self.context, DeviceManagementSettingInstance, ResourcePath("settings", self.resource_path)
            ),
        )

    @odata(name="userStates", navigation=True)
    @property
    def user_states(self) -> EntityCollection[DeviceManagementIntentUserState]:
        """Gets the userStates property"""
        from office365.intune.devices.management_intent_user_state import DeviceManagementIntentUserState

        return self.properties.get(
            "userStates",
            EntityCollection[DeviceManagementIntentUserState](
                self.context, DeviceManagementIntentUserState, ResourcePath("userStates", self.resource_path)
            ),
        )

    @odata(name="userStateSummary", navigation=True)
    @property
    def user_state_summary(self) -> DeviceManagementIntentUserStateSummary:
        """Gets the userStateSummary property"""
        from office365.intune.devices.management_intent_user_state_summary import DeviceManagementIntentUserStateSummary

        return self.properties.get(
            "userStateSummary",
            DeviceManagementIntentUserStateSummary(self.context, ResourcePath("userStateSummary", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementIntent"

    def assign(self, assignments: ClientValueCollection[DeviceManagementIntentAssignment]) -> Self:
        """assign operation.

        Args:
            assignments (ClientValueCollection[DeviceManagementIntentAssignment]):
                assignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, None)
        self.context.add_query(qry)
        return self

    def create_copy(self, display_name: str, description: str) -> DeviceManagementIntent:
        """createCopy operation.

        Args:
            display_name (str):
                displayName parameter
            description (str):
                description parameter
        """
        from office365.intune.devices.management_intent import DeviceManagementIntent

        return_type = DeviceManagementIntent(self.context)
        qry = ServiceOperationQuery(
            self, "createCopy", None, {"displayName": display_name, "description": description}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def migrate_to_template(self, new_template_id: str, preserve_custom_values: bool) -> Self:
        """migrateToTemplate operation.

        Args:
            new_template_id (str):
                newTemplateId parameter
            preserve_custom_values (bool):
                preserveCustomValues parameter
        """
        qry = ServiceOperationQuery(
            self,
            "migrateToTemplate",
            None,
            {"newTemplateId": new_template_id, "preserveCustomValues": preserve_custom_values},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def update_settings(self, settings: ClientValueCollection[DeviceManagementSettingInstance]) -> Self:
        """updateSettings operation.

        Args:
            settings (ClientValueCollection[DeviceManagementSettingInstance]):
                settings parameter
        """
        qry = ServiceOperationQuery(self, "updateSettings", None, {"settings": settings}, None, None)
        self.context.add_query(qry)
        return self
