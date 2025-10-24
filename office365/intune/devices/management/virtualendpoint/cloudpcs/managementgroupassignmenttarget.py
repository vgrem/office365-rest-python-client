from office365.runtime.client_value import ClientValue


class CloudPcManagementGroupAssignmentTarget(ClientValue):

    def __init__(self, group_id: str = None, service_plan_id: str = None):
        self.groupId = group_id
        self.servicePlanId = service_plan_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcManagementGroupAssignmentTarget"
