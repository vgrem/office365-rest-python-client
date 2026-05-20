from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus


@dataclass
class SPSiteCreationResponse(ClientValue):
    SiteId: Optional[str] = None
    SiteStatus: SiteStatus = SiteStatus.None_
    SiteUrl: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"SPSiteCreationResponse("
            f"site_id={self.SiteId!r}, "
            f"site_status={self.SiteStatus!r}, "
            f"site_url={self.SiteUrl!r})"
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SPSiteCreationResponse"
