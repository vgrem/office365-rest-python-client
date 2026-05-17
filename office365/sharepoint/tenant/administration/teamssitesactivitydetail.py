from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class TeamsSitesActivityDetail(ClientValue):
    def __init__(self, last_activity_date: Optional[datetime] = None, team_id: Optional[str] = None):
        self.LastActivityDate = last_activity_date
        self.TeamId = team_id

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TeamsSitesActivityDetail"
