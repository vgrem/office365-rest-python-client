from __future__ import annotations

from typing import Optional

from office365.directory.groups.group import Group
from office365.directory.identitygovernance.privilegedaccess.group_eligibility_schedule import (
    PrivilegedAccessGroupEligibilitySchedule,
)
from office365.directory.identitygovernance.privilegedaccess.groupassignmenttype import (
    PrivilegedAccessGroupAssignmentType,
)
from office365.directory.identitygovernance.privilegedaccess.groupmembertype import PrivilegedAccessGroupMemberType
from office365.directory.identitygovernance.privilegedaccess.grouprelationships import PrivilegedAccessGroupRelationships
from office365.directory.objects.object import DirectoryObject
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class PrivilegedAccessGroupAssignmentSchedule(Entity):
    @property
    def access_id(self) -> PrivilegedAccessGroupRelationships:
        """Gets the accessId property"""
        return self.properties.get("accessId", PrivilegedAccessGroupRelationships.owner)

    @property
    def assignment_type(self) -> PrivilegedAccessGroupAssignmentType:
        """Gets the assignmentType property"""
        return self.properties.get("assignmentType", PrivilegedAccessGroupAssignmentType.assigned)

    @property
    def group_id(self) -> Optional[str]:
        """Gets the groupId property"""
        return self.properties.get("groupId", None)

    @property
    def member_type(self) -> PrivilegedAccessGroupMemberType:
        """Gets the memberType property"""
        return self.properties.get("memberType", PrivilegedAccessGroupMemberType.direct)

    @property
    def principal_id(self) -> Optional[str]:
        """Gets the principalId property"""
        return self.properties.get("principalId", None)

    @property
    def activated_using(self) -> PrivilegedAccessGroupEligibilitySchedule:
        """Gets the activatedUsing property"""
        return self.properties.get(
            "activatedUsing",
            PrivilegedAccessGroupEligibilitySchedule(self.context, ResourcePath("activatedUsing", self.resource_path)),
        )

    @property
    def group(self) -> Group:
        """Gets the group property"""
        return self.properties.get("group", Group(self.context, ResourcePath("group", self.resource_path)))

    @property
    def principal(self) -> DirectoryObject:
        """Gets the principal property"""
        return self.properties.get(
            "principal", DirectoryObject(self.context, ResourcePath("principal", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessGroupAssignmentSchedule"
