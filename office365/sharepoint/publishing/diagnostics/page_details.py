from typing import Optional

from office365.runtime.client_value import ClientValue


class PageDetails(ClientValue):
    def __init__(
        self,
        correlation_id: Optional[str] = None,
        is_published: Optional[bool] = None,
        list_id: Optional[str] = None,
        list_item_id: Optional[int] = None,
        list_item_unique_id: Optional[str] = None,
        page_layout_name: Optional[str] = None,
        page_load_time_in_ms: Optional[int] = None,
        page_type: Optional[str] = None,
        site_id: Optional[str] = None,
        sp_iis_latency_in_ms: Optional[int] = None,
        sp_request_duration_in_ms: Optional[int] = None,
        url: Optional[str] = None,
        version: Optional[str] = None,
        web_id: Optional[str] = None,
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
