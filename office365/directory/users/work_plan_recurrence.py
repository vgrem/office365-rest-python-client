from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.presences.work_location_type import WorkLocationType
    from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
    from office365.outlook.mail.patterned_recurrence import PatternedRecurrence


class WorkPlanRecurrence(Entity):
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

    @odata(name="recurrence")
    @property
    def recurrence(self) -> PatternedRecurrence:
        """Gets the recurrence property"""
        from office365.outlook.mail.patterned_recurrence import PatternedRecurrence

        return self.properties.get("recurrence", PatternedRecurrence())

    @odata(name="start")
    @property
    def start(self) -> DateTimeTimeZone:
        """Gets the start property"""
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("start", DateTimeTimeZone())

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
        return "microsoft.graph.WorkPlanRecurrence"
