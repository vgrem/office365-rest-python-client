from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.dashboard.content import DashboardContent


class DashboardPersonalizationData(ClientValue):
    PersonalizedOrder: DashboardContent = field(default_factory=DashboardContent)
    UserCards: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardPersonalizationData"
