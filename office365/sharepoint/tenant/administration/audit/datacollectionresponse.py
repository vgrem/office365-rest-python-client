from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SPAuditDataCollectionResponse(ClientValue):
    def __init__(
        self,
        data_collection_status: Optional[int] = None,
        opt_in_date_time: Optional[datetime] = None,
        opt_out_date_time: Optional[datetime] = None,
        report_entity: Optional[int] = None,
    ):
        self.DataCollectionStatus = data_collection_status
        self.OptInDateTime = opt_in_date_time
        self.OptOutDateTime = opt_out_date_time
        self.ReportEntity = report_entity

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPAuditDataCollectionResponse"
