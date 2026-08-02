from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.teams.schedule.time_card_break import TimeCardBreak
from office365.teams.schedule.time_card_event import TimeCardEvent


@dataclass
class TimeCardEntry(ClientValue):
    breaks: ClientValueCollection[TimeCardBreak] = field(default_factory=lambda: ClientValueCollection(TimeCardBreak))
    clockInEvent: TimeCardEvent = field(default_factory=TimeCardEvent)
    clockOutEvent: TimeCardEvent = field(default_factory=TimeCardEvent)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeCardEntry"
