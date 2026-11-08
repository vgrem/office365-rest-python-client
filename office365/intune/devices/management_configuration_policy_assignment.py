from __future__ import annotations

from typing import Optional

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)
from office365.entity import Entity
from office365.intune.devices.and_app_management_assignment_source import DeviceAndAppManagementAssignmentSource
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementConfigurationPolicyAssignment(Entity):
    @odata(name="source")
    @property
    def source(self) -> Optional[DeviceAndAppManagementAssignmentSource]:
        """Gets the source property"""
        return self.properties.get("source", None)

    @odata(name="sourceId")
    @property
    def source_id(self) -> Optional[str]:
        """Gets the sourceId property"""
        return self.properties.get("sourceId", None)

    @odata(name="target")
    @property
    def target(self) -> DeviceAndAppManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", DeviceAndAppManagementAssignmentTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationPolicyAssignment"
