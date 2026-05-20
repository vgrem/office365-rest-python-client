from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.noresultitem import ReportNoResultItem


@dataclass
class ReportNoResultQueries(ClientValue):
    Reports: ClientValueCollection[ReportNoResultItem] = field(
        default_factory=lambda: ClientValueCollection(ReportNoResultItem)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNoResultQueries"
