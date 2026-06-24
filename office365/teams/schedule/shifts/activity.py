from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.teams.schedule.entitytheme import ScheduleEntityTheme


class ShiftActivity(ClientValue):
    code: str | None = None
    displayName: str | None = None
    endDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    isPaid: bool | None = None
    startDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    theme: ScheduleEntityTheme = ScheduleEntityTheme.white
    "Represents an activity in a shift."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ShiftActivity"
