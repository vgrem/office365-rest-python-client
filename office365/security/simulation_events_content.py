from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.simulation_event import SimulationEvent


class SimulationEventsContent(ClientValue):
    compromisedRate: float | None = None
    events: ClientValueCollection[SimulationEvent] = field(
        default_factory=lambda: ClientValueCollection(SimulationEvent)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SimulationEventsContent"
