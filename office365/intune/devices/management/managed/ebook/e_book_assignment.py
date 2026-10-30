from __future__ import annotations

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (  # noqa: E501
    DeviceAndAppManagementAssignmentTarget,
)
from office365.entity import Entity
from office365.intune.policies.installintent import InstallIntent
from office365.runtime.types.odata_property import odata


class ManagedEBookAssignment(Entity):
    @odata(name="installIntent")
    @property
    def install_intent(self) -> InstallIntent:
        """Gets the installIntent property"""
        return self.properties.get("installIntent", InstallIntent.available)

    @odata(name="target")
    @property
    def target(self) -> DeviceAndAppManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", DeviceAndAppManagementAssignmentTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedEBookAssignment"
