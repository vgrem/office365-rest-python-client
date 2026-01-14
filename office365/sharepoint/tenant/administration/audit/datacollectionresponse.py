from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPAuditDataCollectionResponse(ClientValue):
    def __init__(
        self,
        data_collection_status: int = None,
        opt_in_date_time: datetime = None,
        opt_out_date_time: datetime = None,
        report_entity: int = None,
    ):
        self.DataCollectionStatus = data_collection_status
        self.OptInDateTime = opt_in_date_time
        self.OptOutDateTime = opt_out_date_time
        self.ReportEntity = report_entity

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPAuditDataCollectionResponse"
