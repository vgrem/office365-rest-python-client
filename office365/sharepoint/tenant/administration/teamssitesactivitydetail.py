from datetime import datetime

from office365.runtime.client_value import ClientValue


class TeamsSitesActivityDetail(ClientValue):

    def __init__(self, last_activity_date: datetime = None, team_id: str = None):
        self.LastActivityDate = last_activity_date
        self.TeamId = team_id

    @property
    def entity_type_name(self):
        return (
            "Microsoft.SharePoint.Administration.TenantAdmin.TeamsSitesActivityDetail"
        )
