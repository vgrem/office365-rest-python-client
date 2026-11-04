from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class QuerySuggestionRange(ClientValue):
    Length: int | None = None
    Start: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionRange"
