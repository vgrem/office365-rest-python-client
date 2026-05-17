from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.noresultitem import ReportNoResultItem


class ReportNoResultQueries(ClientValue):
    def __init__(
        self,
        reports: ClientValueCollection[ReportNoResultItem] = ClientValueCollection(ReportNoResultItem),
    ):
        self.Reports = reports

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNoResultQueries"
