from office365.runtime.client_value import ClientValue


class QuerySuggestionQuery(ClientValue):
    def __init__(self, is_personal: bool = None, query: str = None):
        self.IsPersonal = is_personal
        self.Query = query

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionQuery"
