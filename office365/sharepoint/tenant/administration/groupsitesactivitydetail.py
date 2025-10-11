from datetime import datetime

from office365.runtime.client_value import ClientValue


class GroupSitesActivityDetail(ClientValue):

    def __init__(self, group_id: str = None, last_activity_date: datetime = None):
        self.GroupId = group_id
        self.LastActivityDate = last_activity_date

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.GroupSitesActivityDetail"
