from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus


@dataclass
class GroupSiteInfo(ClientValue):
    """Group site info.

    Fields:
        SiteUrl: Site url.
        SiteStatus: Site status.
    """

    SiteStatus: SiteStatus = SiteStatus.Unknown
    SiteUrl: Optional[str] = None
    DocumentsUrl: Optional[str] = None
    ErrorMessage: Optional[str] = None
    GroupId: Optional[str] = None
    RawSiteProvisionState: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupSiteInfo"
