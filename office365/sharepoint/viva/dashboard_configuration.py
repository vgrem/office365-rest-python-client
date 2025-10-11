from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.query_result import (
    SPClientSideComponentQueryResult,
)
from office365.sharepoint.viva.dashboardcontent import DashboardContent


class DashboardConfiguration(ClientValue):

    def __init__(
        self,
        canvas_content: str = None,
        dashboard_item_id: str = None,
        dashboard_list_id: str = None,
        dashboard_unique_item_id: str = None,
        dashboard_url: str = None,
        extra_components: ClientValueCollection[SPClientSideComponentQueryResult] = ClientValueCollection(
            SPClientSideComponentQueryResult
        ),
        personalization_data: DashboardContent = DashboardContent(),
    ):
        self.canvasContent = canvas_content
        self.dashboardItemId = dashboard_item_id
        self.dashboardListId = dashboard_list_id
        self.dashboardUniqueItemId = dashboard_unique_item_id
        self.dashboardUrl = dashboard_url
        self.extraComponents = extra_components
        self.personalizationData = personalization_data

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.DashboardConfiguration"
