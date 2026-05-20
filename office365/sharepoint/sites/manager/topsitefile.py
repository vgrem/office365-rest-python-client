from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TopSiteFile(ClientValue):
    ContentTypeId: Optional[str] = None
    ListId: Optional[str] = None
    Source: Optional[int] = None
    UniqueId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.TopSiteFile"
