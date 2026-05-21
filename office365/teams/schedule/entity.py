from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class ScheduleEntity(ClientValue):
    endDateTime: datetime = datetime.min
