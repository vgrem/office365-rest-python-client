from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.context_condition import ContextCondition
from office365.sharepoint.search.promotedresults import PromotedResults
from office365.sharepoint.search.query.condition import QueryCondition


@dataclass
class PromotedResultQueryRule(ClientValue):
    """
    This object contains properties that describe one promoted result for the tenant/Search
    Service Application or site collection.
    """

    Contact: str | None = None
    ContextConditions: ClientValueCollection[ContextCondition] = field(
        default_factory=lambda: ClientValueCollection(ContextCondition)
    )
    CreationDate: str | None = None
    DisplayName: str | None = None
    EndDate: datetime | None = None
    IsPromotedResultsOnly: bool | None = None
    LastModifiedDate: datetime | None = None
    PromotedResults: ClientValueCollection[PromotedResults] | None = None
    QueryConditions: ClientValueCollection[QueryCondition] | None = None
    ReviewDate: datetime | None = None
    StartDate: datetime | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResultQueryRule"
