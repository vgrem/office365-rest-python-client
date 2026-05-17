from typing import Optional

from office365.runtime.client_value import ClientValue


class ReportNoResultData(ClientValue):
    def __init__(
        self,
        no_result_percentage: Optional[float] = None,
        query_text: Optional[str] = None,
        result_source: Optional[str] = None,
        total: Optional[int] = None,
    ):
        self.NoResultPercentage = no_result_percentage
        self.QueryText = query_text
        self.ResultSource = result_source
        self.Total = total

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNoResultData"
