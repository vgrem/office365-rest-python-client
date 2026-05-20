from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.query.context import QueryContext


@dataclass
class SearchEndpoints(ClientValue):
    """This property contains the search endpoints."""

    AdminEndpoint: str | None = None
    QueryContext: QueryContext = field(default_factory=QueryContext)
    AfdEndpoint: str | None = None
    Geolocation: str | None = None
    QueryEndpoint: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SearchEndpoints"
