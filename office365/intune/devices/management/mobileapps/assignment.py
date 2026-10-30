from __future__ import annotations

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (  # noqa: E501
    DeviceAndAppManagementAssignmentTarget,
)
from office365.entity import Entity
from office365.intune.devices.management.mobileapps.mobile_app_assignment_settings import MobileAppAssignmentSettings
from office365.intune.policies.installintent import InstallIntent
from office365.runtime.types.odata_property import odata


class MobileAppAssignment(Entity):
    @odata(name="intent")
    @property
    def intent(self) -> InstallIntent:
        """Gets the intent property"""
        return self.properties.get("intent", InstallIntent.available)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppAssignment"

    @odata(name="settings")
    @property
    def settings(self) -> MobileAppAssignmentSettings:
        """Gets the settings property"""
        return self.properties.get("settings", MobileAppAssignmentSettings())

    @odata(name="target")
    @property
    def target(self) -> DeviceAndAppManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", DeviceAndAppManagementAssignmentTarget())
