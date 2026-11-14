from __future__ import annotations

from office365.teams.schedule.shifts.item import ShiftItem


class OpenShiftItem(ShiftItem):
    openSlotCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OpenShiftItem"
