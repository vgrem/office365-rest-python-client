from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.queryrulesitem import ReportQueryRulesItem


class ReportQueryRules(ClientValue):

    def __init__(
        self,
        reports: ClientValueCollection[ReportQueryRulesItem] = ClientValueCollection(
            ReportQueryRulesItem
        ),
    ):
        self.Reports = reports
