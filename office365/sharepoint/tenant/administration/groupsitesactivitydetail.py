from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class GroupSitesActivityDetail(ClientValue):
    def __init__(self, group_id: Optional[str] = None, last_activity_date: Optional[datetime] = None):
        self.GroupId = group_id
        self.LastActivityDate = last_activity_date

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.GroupSitesActivityDetail"
