from datetime import datetime

from office365.runtime.client_value import ClientValue


class RecentAdminActionReport(ClientValue):
    """ """

    def __init__(
        self,
        actions: str = None,
        created_by_email: str = None,
        created_by_name: str = None,
        created_date: datetime = None,
        download_link: str = None,
        name: str = None,
        number_of_records: int = None,
        progress_percentage: float = None,
        query_end_date: datetime = None,
        query_start_date: datetime = None,
        report_type: int = None,
        request_id: str = None,
        sites: str = None,
        s_po_correlation_id: str = None,
        status: int = None,
        u_al_correlation_id: str = None,
        u_al_number_of_records: int = None,
        users: str = None,
    ) -> None:
        self.actions = actions
        self.createdByEmail = created_by_email
        self.createdByName = created_by_name
        self.createdDate = created_date
        self.downloadLink = download_link
        self.name = name
        self.numberOfRecords = number_of_records
        self.progressPercentage = progress_percentage
        self.queryEndDate = query_end_date
        self.queryStartDate = query_start_date
        self.reportType = report_type
        self.requestId = request_id
        self.sites = sites
        self.sPOCorrelationId = s_po_correlation_id
        self.status = status
        self.uALCorrelationId = u_al_correlation_id
        self.uALNumberOfRecords = u_al_number_of_records
        self.users = users

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.RecentAdminActionReport"
