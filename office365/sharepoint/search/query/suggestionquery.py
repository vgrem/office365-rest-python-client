from __future__ import annotations

from office365.runtime.client_value import ClientValue


class QuerySuggestionQuery(ClientValue):
    IsPersonal: bool | None = None
    Query: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionQuery"
