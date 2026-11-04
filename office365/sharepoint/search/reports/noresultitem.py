from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.search.reports.noresultdata import ReportNoResultData


@value
class ReportNoResultItem(ClientValue):
    Date: str | None = None
    Report: ClientValueCollection[ReportNoResultData] = field(
        default_factory=lambda: ClientValueCollection(ReportNoResultData)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportNoResultItem"
