from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.base import ReportBase
from office365.sharepoint.search.reports.topqueries.item import ReportTopQueriesItem


@dataclass
class ReportTopQueries(ReportBase):
    Reports: ClientValueCollection[ReportTopQueriesItem] = field(
        default_factory=lambda: ClientValueCollection(ReportTopQueriesItem)
    )

    @property
    def entity_type_name(self) -> str:  # type: ignore[override]
        return "Microsoft.Office.Server.Search.REST.ReportTopQueries"
