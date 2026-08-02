from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.events.mention_event import MentionEvent
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CallAiInsightViewPoint(ClientValue):
    mentionEvents: ClientValueCollection[MentionEvent] = field(
        default_factory=lambda: ClientValueCollection(MentionEvent)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallAiInsightViewPoint"
