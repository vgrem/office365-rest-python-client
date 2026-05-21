from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class NewsItem(ClientValue):

    backupPictureUrl: Optional[str] = None
    caption: Optional[str] = None
    itemId: Optional[int] = None
    pictureAltText: Optional[str] = None
    pictureUrl: Optional[str] = None
    properties: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.NewsItem"