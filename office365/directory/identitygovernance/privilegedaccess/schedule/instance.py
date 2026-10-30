from datetime import datetime

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PrivilegedAccessScheduleInstance(Entity):
    """An abstract type that exposes properties relating to the instances of membership and ownership assignments
    and eligibilities to groups that are governed by PIM"""

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> datetime:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> datetime:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessScheduleInstance"
