from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class RecentAdminActionReport(ClientValue):
    """ """

    def __init__(
        self,
        actions: Optional[str] = None,
        created_by_email: Optional[str] = None,
        created_by_name: Optional[str] = None,
        created_date: Optional[datetime] = None,
        download_link: Optional[str] = None,
        name: Optional[str] = None,
        number_of_records: Optional[int] = None,
        progress_percentage: Optional[float] = None,
        query_end_date: Optional[datetime] = None,
        query_start_date: Optional[datetime] = None,
        report_type: Optional[int] = None,
        request_id: Optional[str] = None,
        sites: Optional[str] = None,
        s_po_correlation_id: Optional[str] = None,
        status: Optional[int] = None,
        u_al_correlation_id: Optional[str] = None,
        u_al_number_of_records: Optional[int] = None,
        users: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.RecentAdminActionReport"
