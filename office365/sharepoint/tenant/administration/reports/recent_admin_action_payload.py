from datetime import datetime

from office365.runtime.client_value import ClientValue


class RecentAdminActionReportPayload(ClientValue):

    def __init__(
        self,
        actions: str = None,
        name: str = None,
        query_end_date: datetime = None,
        query_start_date: datetime = None,
        report_type: int = None,
        sites: str = None,
        users: str = None,
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
