from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.endpoints import SearchEndpoints
from office365.sharepoint.search.query.context import QueryContext
from office365.sharepoint.search.query.expanded_parameters import (
    ExpandedQueryParameters,
)
from office365.sharepoint.search.query.routing_info import QueryRoutingInfo


@dataclass
class QueryConfiguration(ClientValue):
    """This object contains the query configuration for the local farm and is the response
    to the REST call get query configuration (section 3.1.5.18.2.1.6)."""

    QueryContext: QueryContext = field(default_factory=QueryContext)
    QueryParameters: ExpandedQueryParameters = field(default_factory=ExpandedQueryParameters)
    QueryRoutingInfo: QueryRoutingInfo = field(default_factory=QueryRoutingInfo)
    SearchEndpoints: SearchEndpoints = field(default_factory=SearchEndpoints)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryConfiguration"
