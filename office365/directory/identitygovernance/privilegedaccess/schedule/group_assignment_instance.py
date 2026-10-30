from typing import Optional

from office365.directory.groups.group import Group
from office365.directory.identitygovernance.privilegedaccess.group_eligibility_schedule_instance import (
    PrivilegedAccessGroupEligibilityScheduleInstance,
)
from office365.directory.identitygovernance.privilegedaccess.groupassignmenttype import (
    PrivilegedAccessGroupAssignmentType,
)
from office365.directory.identitygovernance.privilegedaccess.groupmembertype import PrivilegedAccessGroupMemberType
from office365.directory.identitygovernance.privilegedaccess.grouprelationships import PrivilegedAccessGroupRelationships
from office365.directory.identitygovernance.privilegedaccess.schedule.instance import PrivilegedAccessScheduleInstance
from office365.directory.objects.object import DirectoryObject
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class PrivilegedAccessGroupAssignmentScheduleInstance(PrivilegedAccessScheduleInstance):
    """Represents an instance of a provisioned membership or ownership assignment in PIM for groups."""

    @odata(name="accessId")
    @property
    def access_id(self) -> PrivilegedAccessGroupRelationships:
        """Gets the accessId property"""
        return self.properties.get("accessId", PrivilegedAccessGroupRelationships.owner)

    @odata(name="assignmentScheduleId")
    @property
    def assignment_schedule_id(self) -> Optional[str]:
        """Gets the assignmentScheduleId property"""
        return self.properties.get("assignmentScheduleId", None)

    @odata(name="assignmentType")
    @property
    def assignment_type(self) -> PrivilegedAccessGroupAssignmentType:
        """Gets the assignmentType property"""
        return self.properties.get("assignmentType", PrivilegedAccessGroupAssignmentType.assigned)

    @odata(name="groupId")
    @property
    def group_id(self) -> Optional[str]:
        """Gets the groupId property"""
        return self.properties.get("groupId", None)

    @odata(name="memberType")
    @property
    def member_type(self) -> PrivilegedAccessGroupMemberType:
        """Gets the memberType property"""
        return self.properties.get("memberType", PrivilegedAccessGroupMemberType.direct)

    @odata(name="principalId")
    @property
    def principal_id(self) -> Optional[str]:
        """Gets the principalId property"""
        return self.properties.get("principalId", None)

    @odata(name="activatedUsing", navigation=True)
    @property
    def activated_using(self) -> PrivilegedAccessGroupEligibilityScheduleInstance:
        """Gets the activatedUsing property"""
        return self.properties.get(
            "activatedUsing",
            PrivilegedAccessGroupEligibilityScheduleInstance(
                self.context, ResourcePath("activatedUsing", self.resource_path)
            ),
        )

    @odata(name="group", navigation=True)
    @property
    def group(self) -> Group:
        """Gets the group property"""
        return self.properties.get("group", Group(self.context, ResourcePath("group", self.resource_path)))

    @odata(name="principal", navigation=True)
    @property
    def principal(self) -> DirectoryObject:
        """Gets the principal property"""
        return self.properties.get(
            "principal", DirectoryObject(self.context, ResourcePath("principal", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessGroupAssignmentScheduleInstance"
