from __future__ import annotations

from dataclasses import dataclass

from office365.directory.security.triggers.eventpropagationstatus import EventPropagationStatus
from office365.runtime.client_value import ClientValue


@dataclass
class EventPropagationResult(ClientValue):
    location: str | None = None
    serviceName: str | None = None
    status: EventPropagationStatus = EventPropagationStatus.none
    statusInformation: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EventPropagationResult"
