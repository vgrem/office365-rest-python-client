from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.abandonedqueriesdata import (
    ReportAbandonedQueriesData,
)


class ReportAbandonedQueriesItem(ClientValue):
    def __init__(
        self,
        date=None,
        report: ClientValueCollection[ReportAbandonedQueriesData] = ClientValueCollection(ReportAbandonedQueriesData),
    ):
        self.Date = date
        self.Report = report

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportAbandonedQueriesItem"
