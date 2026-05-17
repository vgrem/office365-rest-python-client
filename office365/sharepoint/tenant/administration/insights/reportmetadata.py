from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOInsightsReportMetadata(ClientValue):
    def __init__(
        self, created_date_time_in_utc: Optional[str] = None, id_: Optional[UUID] = None, status: Optional[int] = None
    ):
        self.CreatedDateTimeInUtc = created_date_time_in_utc
        self.Id = id_
        self.Status = status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOInsightsReportMetadata"
