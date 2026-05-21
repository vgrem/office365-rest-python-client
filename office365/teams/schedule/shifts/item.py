from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.teams.schedule.entity import ScheduleEntity
from office365.teams.schedule.shifts.activity import ShiftActivity


@dataclass
class ShiftItem(ScheduleEntity):
    """Represents a version of a shift."""

    displayName: str | None = None
    activities: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(ShiftActivity))
