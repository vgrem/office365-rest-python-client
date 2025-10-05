from office365.runtime.client_value import ClientValue


class ReportNoResultData(ClientValue):

    def __init__(
        self,
        no_result_percentage: float = None,
        query_text: str = None,
        result_source: str = None,
        total: int = None,
    ):
        self.NoResultPercentage = no_result_percentage
        self.QueryText = query_text
        self.ResultSource = result_source
        self.Total = total
