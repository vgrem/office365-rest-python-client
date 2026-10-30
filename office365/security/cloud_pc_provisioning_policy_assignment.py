from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.virtualendpoint.cloudpcs.managementassignmenttarget import (  # noqa: E501
    CloudPcManagementAssignmentTarget,
)
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.users.user import User


class CloudPcProvisioningPolicyAssignment(Entity):
    @odata(name="target")
    @property
    def target(self) -> CloudPcManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", CloudPcManagementAssignmentTarget())

    @odata(name="assignedUsers", navigation=True)
    @property
    def assigned_users(self) -> EntityCollection[User]:
        """Gets the assignedUsers property"""
        from office365.directory.users.user import User

        return self.properties.get(
            "assignedUsers",
            EntityCollection[User](self.context, User, ResourcePath("assignedUsers", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcProvisioningPolicyAssignment"
