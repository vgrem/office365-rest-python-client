from datetime import datetime
from typing import Optional

from office365.entity import Entity


class PrivilegedAccessSchedule(Entity):
    """An abstract type that exposes properties relating to the schedule of assigned and eligible membership and
    ownership to groups that are governed by PIM."""

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def created_using(self) -> Optional[str]:
        """Gets the createdUsing property"""
        return self.properties.get("createdUsing", None)

    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessSchedule"
