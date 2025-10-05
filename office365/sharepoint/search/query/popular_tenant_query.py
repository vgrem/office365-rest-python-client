from office365.runtime.client_value import ClientValue


class PopularTenantQuery(ClientValue):

    def __init__(
        self,
        always_suggest: bool = None,
        click_count: int = None,
        lcid: int = None,
        query_count: int = None,
        query_text: str = None,
        site_id: str = None,
        source_id: str = None,
        web_id: str = None,
    ):
        self.AlwaysSuggest = always_suggest
        self.ClickCount = click_count
        self.LCID = lcid
        self.QueryCount = query_count
        self.QueryText = query_text
        self.SiteId = site_id
        self.SourceId = source_id
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.PopularTenantQuery"
