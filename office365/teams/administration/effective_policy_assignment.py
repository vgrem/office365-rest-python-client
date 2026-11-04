from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.administration.policy_assignment import PolicyAssignment


@value
class EffectivePolicyAssignment(ClientValue):
    policyAssignment: PolicyAssignment = PolicyAssignment()
    policyType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.EffectivePolicyAssignment"
