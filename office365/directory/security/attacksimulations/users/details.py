from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.attacksimulations.user import AttackSimulationUser
from office365.runtime.client_value import ClientValue


@dataclass
class UserSimulationDetails(ClientValue):
    """Represents a user of a tenant and their online actions in an attack simulation and training campaign.

    Args:
        assignedTrainingsCount (int): Number of trainings assigned to a user in an attack simulation and training
          campaign.
        simulationUser (AttackSimulationUser):
    """

    assignedTrainingsCount: int | None = None
    simulationUser: AttackSimulationUser = field(default_factory=AttackSimulationUser)
