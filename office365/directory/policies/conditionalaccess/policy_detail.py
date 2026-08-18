from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.condition_set import ConditionalAccessConditionSet
from office365.directory.policies.conditionalaccess.grant_controls import ConditionalAccessGrantControls
from office365.directory.policies.conditionalaccess.session_controls import ConditionalAccessSessionControls
from office365.runtime.client_value import ClientValue


@dataclass
class ConditionalAccessPolicyDetail(ClientValue):
    conditions: ConditionalAccessConditionSet = field(default_factory=ConditionalAccessConditionSet)
    grantControls: ConditionalAccessGrantControls = field(default_factory=ConditionalAccessGrantControls)
    sessionControls: ConditionalAccessSessionControls = field(default_factory=ConditionalAccessSessionControls)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessPolicyDetail"
