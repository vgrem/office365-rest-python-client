from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RetirablePageMetadata(ClientValue):
    Description: Optional[str] = None
    LastActivityTimestamp: Optional[datetime] = None
    Path: Optional[str] = None
    PictureThumbnailUrl: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.RetirablePageMetadata"
