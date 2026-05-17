from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class RecentAdminActionReportPayload(ClientValue):
    def __init__(
        self,
        actions: Optional[str] = None,
        name: Optional[str] = None,
        query_end_date: Optional[datetime] = None,
        query_start_date: Optional[datetime] = None,
        report_type: Optional[int] = None,
        sites: Optional[str] = None,
        users: Optional[str] = None,
    ):
        self.actions = actions
        self.name = name
        self.queryEndDate = query_end_date
        self.queryStartDate = query_start_date
        self.reportType = report_type
        self.sites = sites
        self.users = users

    " "

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.RecentAdminActionReportPayload"
