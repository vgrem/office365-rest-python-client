from office365.runtime.client_value import ClientValue


class DashboardCardDetails(ClientValue):

    def __init__(
        self, control_index: float = None, instance_id: str = None, state: str = None
    ):
        self.ControlIndex = control_index
        self.InstanceId = instance_id
        self.State = state

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardCardDetails"
