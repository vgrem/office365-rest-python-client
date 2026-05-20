from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.query_result import (
    SPClientSideComponentQueryResult,
)
from office365.sharepoint.viva.dashboard.content import DashboardContent


@dataclass
class DashboardConfiguration(ClientValue):
    canvasContent: Optional[str] = None
    dashboardItemId: Optional[str] = None
    dashboardListId: Optional[str] = None
    dashboardUniqueItemId: Optional[str] = None
    dashboardUrl: Optional[str] = None
    extraComponents: ClientValueCollection[SPClientSideComponentQueryResult] = field(
        default_factory=lambda: ClientValueCollection(SPClientSideComponentQueryResult)
    )
    personalizationData: DashboardContent = field(default_factory=DashboardContent)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.DashboardConfiguration"
