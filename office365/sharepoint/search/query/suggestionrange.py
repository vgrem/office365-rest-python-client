from __future__ import annotations

from office365.runtime.client_value import ClientValue


class QuerySuggestionRange(ClientValue):
    Length: int | None = None
    Start: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionRange"
