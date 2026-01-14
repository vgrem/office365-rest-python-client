from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.collaboration.collaborativeonedriveuser import (
    CollaborativeOneDriveUser,
)
from office365.sharepoint.tenant.administration.collaboration.collaborativeusers import (
    CollaborativeUsers,
)


class CollaborationInsightsData(ClientValue):
    def __init__(
        self,
        last_report_date=None,
        collaborative_users=None,
        collaborative_one_drive_users: ClientValueCollection[CollaborativeOneDriveUser] = ClientValueCollection(
            CollaborativeOneDriveUser
        ),
    ):
        """
        :param str last_report_date:
        :param list[CollaborativeUsers] collaborative_users:
        """
        self.collaborativeUsers = ClientValueCollection(CollaborativeUsers, collaborative_users)
        self.lastReportDate = last_report_date
        self.collaborativeOneDriveUsers = collaborative_one_drive_users

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborationInsightsData"
