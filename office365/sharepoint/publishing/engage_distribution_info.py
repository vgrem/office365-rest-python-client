from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class EngageDistributionInfo(ClientValue):
    DestinationId: str | None = None
    DistributedDate: datetime | None = field(default_factory=lambda: datetime.min)
    RawThreadId: str | None = None
    ThreadId: str | None = None
    ThreadStarterId: str | None = None
    DestinationType: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.EngageDistributionInfo"
