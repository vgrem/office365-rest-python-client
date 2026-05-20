from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ReportQueryRulesData(ClientValue):
    DictionaryTerms: str | None = None
    OwnerType: str | None = None
    PercentagePromotedResult: str | None = None
    PromotedResultClicks: str | None = None
    PromotedResultId: str | None = None
    PromotedResultURL: str | None = None
    PromotedResultURLName: str | None = None
    QueryRule: str | None = None
    QueryRuleId: str | None = None
    ResultSource: str | None = None
    TimesFired: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportQueryRulesData"
