from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.numberofqueriesdata import (
    ReportNumberOfQueriesData,
)


class ReportNumberOfQueriesItem(ClientValue):

    def __init__(
        self,
        date: str = None,
        report: ClientValueCollection[
            ReportNumberOfQueriesData
        ] = ClientValueCollection(ReportNumberOfQueriesData),
    ):
        self.Date = date
        self.Report = report
