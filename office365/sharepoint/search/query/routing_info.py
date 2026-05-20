from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.endpoints import SearchEndpoints


@dataclass
class QueryRoutingInfo(ClientValue):
    """This property contains the query routing info."""

    QueryState: str | None = None
    SearchEndpoints: ClientValueCollection[SearchEndpoints] = field(
        default_factory=lambda: ClientValueCollection(SearchEndpoints)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryRoutingInfo"
