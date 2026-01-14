from datetime import datetime

from office365.runtime.client_value import ClientValue


class CollaborationInsightsOverview(ClientValue):
    def __init__(
        self,
        last_report_date: datetime = None,
        total_guests: int = None,
        total_internal_users: int = None,
        total_one_drives: int = None,
        total_sites: int = None,
        total_users: int = None,
    ):
        self.lastReportDate = last_report_date
        self.totalGuests = total_guests
        self.totalInternalUsers = total_internal_users
        self.totalOneDrives = total_one_drives
        self.totalSites = total_sites
        self.totalUsers = total_users

    ""

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborationInsightsOverview"
