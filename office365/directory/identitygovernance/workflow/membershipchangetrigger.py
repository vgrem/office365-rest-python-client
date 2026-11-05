from __future__ import annotations

from office365.directory.identitygovernance.workflow.membershiptype import MembershipChangeType
from office365.runtime.client_value import ClientValue


class MembershipChangeTrigger(ClientValue):
    changeType: MembershipChangeType | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.MembershipChangeTrigger"
