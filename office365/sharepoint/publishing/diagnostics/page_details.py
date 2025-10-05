from office365.runtime.client_value import ClientValue


class PageDetails(ClientValue):

    def __init__(
        self,
        correlation_id: str = None,
        is_published: bool = None,
        list_id: str = None,
        list_item_id: int = None,
        list_item_unique_id: str = None,
        page_layout_name: str = None,
        page_load_time_in_ms: int = None,
        page_type: str = None,
        site_id: str = None,
        sp_iis_latency_in_ms: int = None,
        sp_request_duration_in_ms: int = None,
        url: str = None,
        version: str = None,
        web_id: str = None,
    ):
        self.CorrelationId = correlation_id
        self.IsPublished = is_published
        self.ListId = list_id
        self.ListItemId = list_item_id
        self.ListItemUniqueId = list_item_unique_id
        self.PageLayoutName = page_layout_name
        self.PageLoadTimeInMS = page_load_time_in_ms
        self.PageType = page_type
        self.SiteId = site_id
        self.SpIISLatencyInMS = sp_iis_latency_in_ms
        self.SpRequestDurationInMS = sp_request_duration_in_ms
        self.Url = url
        self.Version = version
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.PageDetails"
