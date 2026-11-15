from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class GroupPolicyConfigurationAssignment(Entity):
    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="target")
    @property
    def target(self) -> DeviceAndAppManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", DeviceAndAppManagementAssignmentTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyConfigurationAssignment"
