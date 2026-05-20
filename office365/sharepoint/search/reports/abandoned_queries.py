from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.abandonedqueries.item import (
    ReportAbandonedQueriesItem,
)
from office365.sharepoint.search.reports.base import ReportBase


@dataclass
class ReportAbandonedQueries(ReportBase):
    """This report shows popular search queries that receive low click-through. Use this report to identify search
    queries that might create user dissatisfaction and to improve the discoverability of content.
    """

    Reports: ClientValueCollection[ReportAbandonedQueriesItem] = field(
        default_factory=lambda: ClientValueCollection(ReportAbandonedQueriesItem)
    )

    @property
    def entity_type_name(self) -> str:  # type: ignore[override]
        return "Microsoft.Office.Server.Search.REST.ReportAbandonedQueries"
