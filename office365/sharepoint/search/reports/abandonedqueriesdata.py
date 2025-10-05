from office365.runtime.client_value import ClientValue


class ReportAbandonedQueriesData(ClientValue):

    def __init__(
        self,
        abandoned_percentage: float = None,
        query_text: str = None,
        result_source: str = None,
        total: int = None,
    ):
        self.AbandonedPercentage = abandoned_percentage
        self.QueryText = query_text
        self.ResultSource = result_source
        self.Total = total

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportAbandonedQueriesData"
