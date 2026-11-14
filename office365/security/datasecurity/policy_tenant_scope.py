from __future__ import annotations

from dataclasses import field

from office365.security.datasecurity.policy_binding import PolicyBinding
from office365.security.datasecurity.policy_scope_base import PolicyScopeBase


class PolicyTenantScope(PolicyScopeBase):
    policyScope: PolicyBinding = field(default_factory=PolicyBinding)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyTenantScope"
