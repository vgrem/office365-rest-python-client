from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.queryrulesitem import ReportQueryRulesItem


@dataclass
class ReportQueryRules(ClientValue):
    Reports: ClientValueCollection[ReportQueryRulesItem] = field(
        default_factory=lambda: ClientValueCollection(ReportQueryRulesItem)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportQueryRules"
