from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.presences.work_location_type import WorkLocationType
    from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
    from office365.teams.schedule.time_off_details import TimeOffDetails


class WorkPlanOccurrence(Entity):
    @odata(name="end")
    @property
    def end(self) -> DateTimeTimeZone:
        """Gets the end property"""
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("end", DateTimeTimeZone())

    @odata(name="placeId")
    @property
    def place_id(self) -> Optional[str]:
        """Gets the placeId property"""
        return self.properties.get("placeId", None)

    @odata(name="recurrenceId")
    @property
    def recurrence_id(self) -> Optional[str]:
        """Gets the recurrenceId property"""
        return self.properties.get("recurrenceId", None)

    @odata(name="start")
    @property
    def start(self) -> DateTimeTimeZone:
        """Gets the start property"""
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("start", DateTimeTimeZone())

    @odata(name="timeOffDetails")
    @property
    def time_off_details(self) -> TimeOffDetails:
        """Gets the timeOffDetails property"""
        from office365.teams.schedule.time_off_details import TimeOffDetails

        return self.properties.get("timeOffDetails", TimeOffDetails())

    @odata(name="workLocationType")
    @property
    def work_location_type(self) -> WorkLocationType:
        """Gets the workLocationType property"""
        from office365.communications.presences.work_location_type import (
            WorkLocationType,
        )

        return self.properties.get("workLocationType", WorkLocationType.unspecified)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkPlanOccurrence"
