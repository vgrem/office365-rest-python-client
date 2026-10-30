from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.virtualendpoint.cloudpcs.managementassignmenttarget import (  # noqa: E501
    CloudPcManagementAssignmentTarget,
)
from office365.runtime.types.odata_property import odata


class CloudPcUserSettingAssignment(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="target")
    @property
    def target(self) -> CloudPcManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", CloudPcManagementAssignmentTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcUserSettingAssignment"
