from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class TopSiteFile(ClientValue):
    ContentTypeId: Optional[str] = None
    ListId: Optional[str] = None
    Source: Optional[int] = None
    UniqueId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.TopSiteFile"
