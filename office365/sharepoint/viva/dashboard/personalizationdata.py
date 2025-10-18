from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.dashboard.content import DashboardContent


class DashboardPersonalizationData(ClientValue):

    def __init__(
        self,
        personalized_order: DashboardContent = DashboardContent(),
        user_cards: str = None,
    ):
        self.PersonalizedOrder = personalized_order
        self.UserCards = user_cards

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.DashboardPersonalizationData"
