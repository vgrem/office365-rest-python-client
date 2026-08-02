from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_value import ClientValue


@dataclass
class TimeCardEvent(ClientValue):
    dateTime: datetime | None = field(default_factory=lambda: datetime.min)
    isAtApprovedLocation: bool | None = None
    notes: ItemBody = field(default_factory=ItemBody)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeCardEvent"
