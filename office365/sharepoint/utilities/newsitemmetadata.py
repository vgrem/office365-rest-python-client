from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class NewsItemMetaData(ClientValue):
    def __init__(
        self,
        file_extension: Optional[str] = None,
        news_type: Optional[int] = None,
        prog_id: Optional[str] = None,
        site_id: Optional[UUID] = None,
        title: Optional[str] = None,
        unique_id: Optional[UUID] = None,
        url: Optional[str] = None,
        web_id: Optional[UUID] = None,
    ):
        self.fileExtension = file_extension
        self.newsType = news_type
        self.progId = prog_id
        self.siteId = site_id
        self.title = title
        self.uniqueId = unique_id
        self.url = url
        self.webId = web_id

    @property
    def entity_type_name(self):
        return "SP.Utilities.NewsItemMetaData"
