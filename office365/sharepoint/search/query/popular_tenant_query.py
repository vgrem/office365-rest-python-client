from typing import Optional

from office365.runtime.client_value import ClientValue


class PopularTenantQuery(ClientValue):
    def __init__(
        self,
        always_suggest: Optional[bool] = None,
        click_count: Optional[int] = None,
        lcid: Optional[int] = None,
        query_count: Optional[int] = None,
        query_text: Optional[str] = None,
        site_id: Optional[str] = None,
        source_id: Optional[str] = None,
        web_id: Optional[str] = None,
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
