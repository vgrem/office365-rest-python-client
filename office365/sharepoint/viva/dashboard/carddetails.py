from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class DashboardCardDetails(ClientValue):
    ControlIndex: Optional[float] = None
    InstanceId: Optional[str] = None
    State: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardCardDetails"
