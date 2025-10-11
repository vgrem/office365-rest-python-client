from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.queryrulesdata import ReportQueryRulesData


class ReportQueryRulesItem(ClientValue):

    def __init__(
        self,
        date: str = None,
        report: ClientValueCollection[ReportQueryRulesData] = ClientValueCollection(ReportQueryRulesData),
    ):
        self.Date = date
        self.Report = report

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportQueryRulesItem"
