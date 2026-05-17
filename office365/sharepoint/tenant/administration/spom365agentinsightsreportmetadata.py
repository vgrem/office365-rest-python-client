from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOM365AgentInsightsReportMetadata(ClientValue):
    def __init__(
        self,
        created_date_time_in_utc: Optional[str] = None,
        id_: Optional[UUID] = None,
        report_period_in_days: Optional[int] = None,
        status: Optional[int] = None,
    ):
        self.CreatedDateTimeInUtc = created_date_time_in_utc
        self.Id = id_
        self.ReportPeriodInDays = report_period_in_days
        self.Status = status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOM365AgentInsightsReportMetadata"
