from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.diagnostics.page_details import PageDetails
from office365.sharepoint.publishing.ruleresult import RuleResult
from office365.sharepoint.publishing.tooldetails import ToolDetails


class PageDiagnosticsResult(ClientValue):

    def __init__(
        self,
        created_date: datetime = None,
        page_details: PageDetails = PageDetails(),
        result_status: int = None,
        suggestions: ClientValueCollection[RuleResult] = ClientValueCollection(RuleResult),
        score: int = None,
        tool_details: ToolDetails = ToolDetails(),
    ):
        self.CreatedDate = created_date
        self.PageDetails = page_details
        self.ResultStatus = result_status
        self.suggestions = suggestions
        self.Score = score
        self.ToolDetails = tool_details

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.PageDiagnosticsResult"
