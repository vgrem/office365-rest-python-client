from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ReportAbandonedQueriesData(ClientValue):
    AbandonedPercentage: float | None = None
    QueryText: str | None = None
    ResultSource: str | None = None
    Total: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportAbandonedQueriesData"
