from office365.runtime.client_value import ClientValue


class ReportTopQueriesData(ClientValue):
    def __init__(
        self,
        query_percentage: float = None,
        query_text: str = None,
        result_source: str = None,
        total: int = None,
    ):
        self.QueryPercentage = query_percentage
        self.QueryText = query_text
        self.ResultSource = result_source
        self.Total = total

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportTopQueriesData"
