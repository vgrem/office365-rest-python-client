from office365.runtime.client_value import ClientValue
from typing import Optional


class DashboardCardDetails(ClientValue):
    def __init__(
        self, control_index: Optional[float] = None, instance_id: Optional[str] = None, state: Optional[str] = None
    ):
        self.ControlIndex = control_index
        self.InstanceId = instance_id
        self.State = state

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardCardDetails"
