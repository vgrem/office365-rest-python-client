from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class CustomQuerySuggestions(ClientValue):

    def __init__(
        self, lcid: int = None, queries: StringCollection = StringCollection()
    ):
        self.LCID = lcid
        self.Queries = queries

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.CustomQuerySuggestions"
