from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.news.itemreference import NewsItemReference as ItemReference


@dataclass
class NewsSite(ClientValue):
    Acronym: Optional[str] = None
    BannerColor: Optional[str] = None
    BannerImageUrl: Optional[str] = None
    ItemReference: ItemReference = field(default_factory=ItemReference)
    Title: Optional[str] = None
    Type: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.NewsSite"
