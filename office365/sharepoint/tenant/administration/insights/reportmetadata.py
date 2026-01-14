from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOInsightsReportMetadata(ClientValue):
    def __init__(self, created_date_time_in_utc: str = None, id_: UUID = None, status: int = None):
        self.CreatedDateTimeInUtc = created_date_time_in_utc
        self.Id = id_
        self.Status = status

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOInsightsReportMetadata"
