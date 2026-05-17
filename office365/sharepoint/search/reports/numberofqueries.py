from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.numberofqueriesitem import (
    ReportNumberOfQueriesItem,
)


class ReportNumberOfQueries(ClientValue):
    def __init__(
        self,
        reports: ClientValueCollection[ReportNumberOfQueriesItem] = ClientValueCollection(ReportNumberOfQueriesItem),
    ):
        self.Reports = reports

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNumberOfQueries"
