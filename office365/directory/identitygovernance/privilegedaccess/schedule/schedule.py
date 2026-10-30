from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.request_schedule import RequestSchedule
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PrivilegedAccessSchedule(Entity):
    """An abstract type that exposes properties relating to the schedule of assigned and eligible membership and
    ownership to groups that are governed by PIM."""

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="createdUsing")
    @property
    def created_using(self) -> Optional[str]:
        """Gets the createdUsing property"""
        return self.properties.get("createdUsing", None)

    @odata(name="modifiedDateTime")
    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessSchedule"

    @odata(name="scheduleInfo")
    @property
    def schedule_info(self) -> RequestSchedule:
        """Gets the scheduleInfo property"""
        return self.properties.get("scheduleInfo", RequestSchedule())
