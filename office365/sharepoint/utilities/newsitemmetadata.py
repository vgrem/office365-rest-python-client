from __future__ import annotations

from typing import Optional
from uuid import UUID


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class NewsItemMetaData(ClientValue):

    fileExtension: Optional[str] = None
    newsType: Optional[int] = None
    progId: Optional[str] = None
    siteId: Optional[UUID] = None
    title: Optional[str] = None
    uniqueId: Optional[UUID] = None
    url: Optional[str] = None
    webId: Optional[UUID] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.NewsItemMetaData"