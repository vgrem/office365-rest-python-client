from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.noresultdata import ReportNoResultData


class ReportNoResultItem(ClientValue):

    def __init__(
        self,
        date: str = None,
        report: ClientValueCollection[ReportNoResultData] = ClientValueCollection(
            ReportNoResultData
        ),
    ):
        self.Date = date
        self.Report = report
