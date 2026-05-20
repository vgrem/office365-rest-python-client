from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.object_owner_result import SearchObjectOwnerResult
from office365.sharepoint.search.promoted_result_query_rule import (
    PromotedResultQueryRule,
)


@dataclass
class PromotedResultsOperationsResult(ClientValue):
    """This object contains properties that describes the result of the REST call get promoted results"""

    Result: ClientValueCollection[PromotedResultQueryRule] = field(
        default_factory=lambda: ClientValueCollection(PromotedResultQueryRule)
    )
    SearchObjectOwner: SearchObjectOwnerResult = field(default_factory=SearchObjectOwnerResult)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResultsOperationsResult"
