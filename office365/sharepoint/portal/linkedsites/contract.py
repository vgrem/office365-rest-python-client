from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class LinkedSiteContract(ClientValue):
    DisplayName: Optional[str] = None
    GroupId: Optional[str] = None
    PictureUrl: Optional[str] = None
    SiteId: Optional[str] = None
    Url: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.LinkedSiteContract"
