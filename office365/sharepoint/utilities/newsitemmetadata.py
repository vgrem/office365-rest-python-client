from uuid import UUID

from office365.runtime.client_value import ClientValue


class NewsItemMetaData(ClientValue):

    def __init__(
        self,
        file_extension: str = None,
        news_type: int = None,
        prog_id: str = None,
        site_id: UUID = None,
        title: str = None,
        unique_id: UUID = None,
        url: str = None,
        web_id: UUID = None,
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
