from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class NewsItemReference(ClientValue):
    ItemId: Optional[int] = None
    LibraryId: Optional[str] = None
    SiteId: Optional[str] = None
    WebId: Optional[str] = None
    Type: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.News.DataModel.ItemReference"
