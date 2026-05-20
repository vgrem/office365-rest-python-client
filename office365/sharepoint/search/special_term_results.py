from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.special_term_result import SpecialTermResult


@dataclass
class SpecialTermResults(ClientValue):
    """The SpecialTermResults table contains best bets that apply to the search query."""

    Results: ClientValueCollection[SpecialTermResult] = field(
        default_factory=lambda: ClientValueCollection(SpecialTermResult)
    )
    GroupTemplateId: str | None = None
    ItemTemplateId: str | None = None
    Properties: dict | None = None
    ResultTitle: str | None = None
    ResultTitleUrl: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SpecialTermResults"
