from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
        DeviceAndAppManagementAssignmentTarget,
    )


class ManagedDeviceMobileAppConfigurationAssignment(Entity):
    @odata(name="target")
    @property
    def target(self) -> DeviceAndAppManagementAssignmentTarget:
        """Gets the target property"""
        from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
            DeviceAndAppManagementAssignmentTarget,
        )

        return self.properties.get("target", DeviceAndAppManagementAssignmentTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedDeviceMobileAppConfigurationAssignment"
