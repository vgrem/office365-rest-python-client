from office365.runtime.client_value import ClientValue


class ReportNumberOfQueriesData(ClientValue):
    def __init__(self, hits: str = None, result_source: str = None, total_queries: str = None):
        self.Hits = hits
        self.ResultSource = result_source
        self.TotalQueries = total_queries

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNumberOfQueriesData"
