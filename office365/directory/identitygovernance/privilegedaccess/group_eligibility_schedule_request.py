from __future__ import annotations

from typing import Optional

from office365.directory.groups.group import Group
from office365.directory.identitygovernance.privilegedaccess.group_eligibility_schedule import (
    PrivilegedAccessGroupEligibilitySchedule,
)
from office365.directory.identitygovernance.privilegedaccess.grouprelationships import PrivilegedAccessGroupRelationships
from office365.directory.objects.object import DirectoryObject
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class PrivilegedAccessGroupEligibilityScheduleRequest(Entity):
    @odata(name="accessId")
    @property
    def access_id(self) -> PrivilegedAccessGroupRelationships:
        """Gets the accessId property"""
        return self.properties.get("accessId", PrivilegedAccessGroupRelationships.owner)

    @odata(name="groupId")
    @property
    def group_id(self) -> Optional[str]:
        """Gets the groupId property"""
        return self.properties.get("groupId", None)

    @odata(name="principalId")
    @property
    def principal_id(self) -> Optional[str]:
        """Gets the principalId property"""
        return self.properties.get("principalId", None)

    @odata(name="targetScheduleId")
    @property
    def target_schedule_id(self) -> Optional[str]:
        """Gets the targetScheduleId property"""
        return self.properties.get("targetScheduleId", None)

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

    @odata(name="targetSchedule", navigation=True)
    @property
    def target_schedule(self) -> PrivilegedAccessGroupEligibilitySchedule:
        """Gets the targetSchedule property"""
        return self.properties.get(
            "targetSchedule",
            PrivilegedAccessGroupEligibilitySchedule(self.context, ResourcePath("targetSchedule", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessGroupEligibilityScheduleRequest"
