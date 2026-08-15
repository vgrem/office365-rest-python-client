from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from office365.directory.synchronization.schedulestate import SynchronizationScheduleState
from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationSchedule(ClientValue):
    expiration: datetime | None = field(default_factory=lambda: datetime.min)
    interval: timedelta | None = None
    state: SynchronizationScheduleState = SynchronizationScheduleState.Active

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationSchedule"
