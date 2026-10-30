from __future__ import annotations

from typing import Optional

from office365.directory.request_schedule import RequestSchedule
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UnifiedRoleEligibilitySchedule(Entity):
    @odata(name="memberType")
    @property
    def member_type(self) -> Optional[str]:
        """Gets the memberType property"""
        return self.properties.get("memberType", None)

    @odata(name="scheduleInfo")
    @property
    def schedule_info(self) -> RequestSchedule:
        """Gets the scheduleInfo property"""
        return self.properties.get("scheduleInfo", RequestSchedule())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleEligibilitySchedule"
