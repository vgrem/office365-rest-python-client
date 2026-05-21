from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.diagnostics.page_details import PageDetails as _PageDetails
from office365.sharepoint.publishing.ruleresult import RuleResult
from office365.sharepoint.publishing.tooldetails import ToolDetails as _ToolDetails


@dataclass
class PageDiagnosticsResult(ClientValue):
    CreatedDate: Optional[datetime] = None
    PageDetails: _PageDetails = field(default_factory=lambda: _PageDetails())
    ResultStatus: Optional[int] = None
    suggestions: ClientValueCollection[RuleResult] = field(default_factory=lambda: ClientValueCollection(RuleResult))
    Score: Optional[int] = None
    ToolDetails: _ToolDetails = field(default_factory=lambda: _ToolDetails())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.PageDiagnosticsResult"
