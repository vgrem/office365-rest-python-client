from typing import Optional

from office365.runtime.client_value import ClientValue


class ReportTopQueriesData(ClientValue):
    def __init__(
        self,
        query_percentage: Optional[float] = None,
        query_text: Optional[str] = None,
        result_source: Optional[str] = None,
        total: Optional[int] = None,
    ):
        self.QueryPercentage = query_percentage
        self.QueryText = query_text
        self.ResultSource = result_source
        self.Total = total

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportTopQueriesData"
