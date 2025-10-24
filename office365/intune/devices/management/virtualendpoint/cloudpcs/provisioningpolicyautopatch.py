from office365.runtime.client_value import ClientValue


class CloudPcProvisioningPolicyAutopatch(ClientValue):

    def __init__(self, autopatch_group_id: str = None):
        self.autopatchGroupId = autopatch_group_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcProvisioningPolicyAutopatch"
