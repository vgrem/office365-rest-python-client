from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DashboardCardDetails(ClientValue):
    ControlIndex: Optional[float] = None
    InstanceId: Optional[str] = None
    State: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardCardDetails"
