from typing import Optional

from office365.runtime.client_value import ClientValue


class ReportNumberOfQueriesData(ClientValue):
    def __init__(
        self, hits: Optional[str] = None, result_source: Optional[str] = None, total_queries: Optional[str] = None
    ):
        self.Hits = hits
        self.ResultSource = result_source
        self.TotalQueries = total_queries

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNumberOfQueriesData"
