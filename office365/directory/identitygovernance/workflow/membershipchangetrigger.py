from office365.directory.identitygovernance.workflow.membershiptype import MembershipChangeType
from office365.runtime.client_value import ClientValue


class MembershipChangeTrigger(ClientValue):

    def __init__(self, change_type: MembershipChangeType = None):
        self.changeType = change_type

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.MembershipChangeTrigger"
