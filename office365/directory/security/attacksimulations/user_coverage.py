from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AttackSimulationSimulationUserCoverage(ClientValue):
    """Represents cumulative simulation data and results for a user in attack simulation and training."""
