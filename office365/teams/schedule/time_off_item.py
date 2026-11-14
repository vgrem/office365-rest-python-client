from __future__ import annotations

from office365.teams.schedule.entity import ScheduleEntity


class TimeOffItem(ScheduleEntity):
    timeOffReasonId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeOffItem"
