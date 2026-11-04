from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.schedule.entitytheme import ScheduleEntityTheme


@value
class ScheduleEntity(ClientValue):
    endDateTime: datetime = datetime.min
    startDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    theme: ScheduleEntityTheme = ScheduleEntityTheme.white

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ScheduleEntity"
