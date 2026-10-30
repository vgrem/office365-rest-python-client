from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.attacksimulations.simulationautomationrunstatus import (
        SimulationAutomationRunStatus,
    )


class SimulationAutomationRun(Entity):
    """Represents a run of an attack simulation automation on a tenant."""

    @odata(name="simulationId")
    @property
    def simulation_id(self) -> Optional[str]:
        """"""
        return self.properties.get("simulationId", None)

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> Optional[datetime]:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> SimulationAutomationRunStatus:
        """Gets the status property"""
        from office365.security.attacksimulations.simulationautomationrunstatus import (
            SimulationAutomationRunStatus,
        )

        return self.properties.get("status", SimulationAutomationRunStatus.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SimulationAutomationRun"
