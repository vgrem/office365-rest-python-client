from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.dashboard.carddetails import DashboardCardDetails


class DashboardContent(ClientValue):

    def __init__(
        self,
        dashboard_card_details: ClientValueCollection[DashboardCardDetails] = ClientValueCollection(
            DashboardCardDetails
        ),
        dashboard_form_factor: str = None,
        dashboard_id: str = None,
        last_modified_date: datetime = None,
    ):
        self.DashboardCardDetails = dashboard_card_details
        self.DashboardFormFactor = dashboard_form_factor
        self.DashboardId = dashboard_id
        self.LastModifiedDate = last_modified_date

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardContent"
