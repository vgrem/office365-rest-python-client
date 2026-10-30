from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TimeOffRequest(Entity):
    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> Optional[datetime]:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="timeOffReasonId")
    @property
    def time_off_reason_id(self) -> Optional[str]:
        """Gets the timeOffReasonId property"""
        return self.properties.get("timeOffReasonId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeOffRequest"
