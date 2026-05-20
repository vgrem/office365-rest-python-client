from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.reports.numberofqueriesdata import (
    ReportNumberOfQueriesData,
)


@dataclass
class ReportNumberOfQueriesItem(ClientValue):
    Date: str | None = None
    Report: ClientValueCollection[ReportNumberOfQueriesData] = field(
        default_factory=lambda: ClientValueCollection(ReportNumberOfQueriesData)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNumberOfQueriesItem"
