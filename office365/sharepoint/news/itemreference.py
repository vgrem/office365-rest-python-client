from typing import Optional

from office365.runtime.client_value import ClientValue


class NewsItemReference(ClientValue):
    def __init__(
        self,
        item_id: Optional[int] = None,
        library_id: Optional[str] = None,
        site_id: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        super().__init__()
        self.ItemId = item_id
        self.LibraryId = library_id
        self.SiteId = site_id
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.News.DataModel.ItemReference"
