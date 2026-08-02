from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_value import ClientValue
from office365.teams.schedule.time_card_event import TimeCardEvent


@dataclass
class TimeCardBreak(ClientValue):
    breakId: str | None = None
    end: TimeCardEvent = field(default_factory=TimeCardEvent)
    notes: ItemBody = field(default_factory=ItemBody)
    start: TimeCardEvent = field(default_factory=TimeCardEvent)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeCardBreak"
