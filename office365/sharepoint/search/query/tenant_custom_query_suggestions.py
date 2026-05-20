from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.query.customsuggestions import CustomQuerySuggestions


@dataclass
class TenantCustomQuerySuggestions(ClientValue):
    AlwaysSuggest: ClientValueCollection[CustomQuerySuggestions] = field(
        default_factory=lambda: ClientValueCollection(CustomQuerySuggestions)
    )
    NeverSuggest: ClientValueCollection[CustomQuerySuggestions] = field(
        default_factory=lambda: ClientValueCollection(CustomQuerySuggestions)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.TenantCustomQuerySuggestions"
