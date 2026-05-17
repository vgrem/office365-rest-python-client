from typing import Optional

from office365.runtime.client_value import ClientValue


class QuerySuggestionRange(ClientValue):
    def __init__(self, length: Optional[int] = None, start: Optional[int] = None):
        self.Length = length
        self.Start = start

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionRange"
