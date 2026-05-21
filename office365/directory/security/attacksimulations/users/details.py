from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.attacksimulations.user import AttackSimulationUser
from office365.runtime.client_value import ClientValue


@dataclass
class UserSimulationDetails(ClientValue):
    """Represents a user of a tenant and their online actions in an attack simulation and training campaign.

    :param int assigned_trainings_count: Number of trainings assigned to a user in an attack simulation
        and training campaign.
    :param AttackSimulationUser simulation_user:
    """

    assignedTrainingsCount: int | None = None
    simulationUser: AttackSimulationUser = field(default_factory=AttackSimulationUser)
