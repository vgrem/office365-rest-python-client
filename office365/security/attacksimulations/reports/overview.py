from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.search.recommended_action import RecommendedAction
from office365.security.attacksimulations.event import TrainingEventsContent
from office365.security.simulation_events_content import (
    SimulationEventsContent,
)


@value
class SimulationReportOverview(ClientValue):
    """Represents an overview report of an attack simulation and training campaign."""

    resolvedTargetsCount: int | None = None

    simulationEventsContent: SimulationEventsContent = field(default_factory=SimulationEventsContent)

    trainingEventsContent: TrainingEventsContent = field(default_factory=TrainingEventsContent)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SimulationReportOverview"

    recommendedActions: ClientValueCollection[RecommendedAction] = field(
        default_factory=lambda: ClientValueCollection(RecommendedAction)
    )
