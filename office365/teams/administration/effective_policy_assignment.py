from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.teams.administration.policy_assignment import PolicyAssignment


class EffectivePolicyAssignment(ClientValue):
    policyAssignment: PolicyAssignment = field(default_factory=PolicyAssignment)
    policyType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.EffectivePolicyAssignment"
