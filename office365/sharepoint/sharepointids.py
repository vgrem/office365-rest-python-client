from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SharePointIds(ClientValue):
    hub_site_id: Optional[str] = None
    site_id: Optional[str] = None
    site_url: Optional[str] = None
    web_id: Optional[str] = None
    listId: Optional[str] = None
    uniqueId: Optional[str] = None
    listItemId: Optional[str] = None
    listItemUniqueId: Optional[str] = None
    tenantId: Optional[str] = None
    HubSiteId: str | None = None
    SiteId: str | None = None
    SiteUrl: str | None = None
    WebId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.SharePointIds"
