from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.query.property_value import QueryPropertyValue


@dataclass
class QueryProperty(ClientValue):
    """This object stores additional or custom properties for a search query. A QueryProperty is structured
    as name-value pairs."""

    Name: str | None = None
    Value: QueryPropertyValue = field(default_factory=QueryPropertyValue)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QueryPropertyValue"
