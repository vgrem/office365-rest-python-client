from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.abandonedqueriesdata import (
    ReportAbandonedQueriesData,
)


@dataclass
class ReportAbandonedQueriesItem(ClientValue):
    Date: str | None = None
    Report: ClientValueCollection[ReportAbandonedQueriesData] = field(
        default_factory=lambda: ClientValueCollection(ReportAbandonedQueriesData)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportAbandonedQueriesItem"
