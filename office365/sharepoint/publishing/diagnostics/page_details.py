from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PageDetails(ClientValue):
    CorrelationId: Optional[str] = None
    IsPublished: Optional[bool] = None
    ListId: Optional[str] = None
    ListItemId: Optional[int] = None
    ListItemUniqueId: Optional[str] = None
    PageLayoutName: Optional[str] = None
    PageLoadTimeInMS: Optional[int] = None
    PageType: Optional[str] = None
    SiteId: Optional[str] = None
    SpIISLatencyInMS: Optional[int] = None
    SpRequestDurationInMS: Optional[int] = None
    Url: Optional[str] = None
    Version: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.PageDetails"
