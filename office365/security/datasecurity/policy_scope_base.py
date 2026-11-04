from __future__ import annotations

from dataclasses import field

from office365.directory.policies.executionmode import ExecutionMode
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.security.datasecurity.dlp_action_info import DlpActionInfo
from office365.security.datasecurity.policy_location import PolicyLocation
from office365.security.useractivitytypes import UserActivityTypes


@value
class PolicyScopeBase(ClientValue):
    activities: UserActivityTypes = UserActivityTypes.none
    executionMode: ExecutionMode = ExecutionMode.evaluateInline
    locations: ClientValueCollection[PolicyLocation] = field(
        default_factory=lambda: ClientValueCollection(PolicyLocation)
    )
    policyActions: ClientValueCollection[DlpActionInfo] = field(
        default_factory=lambda: ClientValueCollection(DlpActionInfo)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyScopeBase"
