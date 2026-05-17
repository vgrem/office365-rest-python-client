from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.query.customsuggestions import CustomQuerySuggestions


class TenantCustomQuerySuggestions(ClientValue):
    def __init__(
        self,
        always_suggest: ClientValueCollection[CustomQuerySuggestions] = ClientValueCollection(CustomQuerySuggestions),
        never_suggest: ClientValueCollection[CustomQuerySuggestions] = ClientValueCollection(CustomQuerySuggestions),
    ):
        self.AlwaysSuggest = always_suggest
        self.NeverSuggest = never_suggest

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.TenantCustomQuerySuggestions"
