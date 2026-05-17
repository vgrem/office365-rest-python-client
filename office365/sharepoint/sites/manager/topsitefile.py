from office365.runtime.client_value import ClientValue
from typing import Optional


class TopSiteFile(ClientValue):
    def __init__(
        self,
        content_type_id: Optional[str] = None,
        list_id: Optional[str] = None,
        source: Optional[int] = None,
        unique_id: Optional[str] = None,
    ):
        self.ContentTypeId = content_type_id
        self.ListId = list_id
        self.Source = source
        self.UniqueId = unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.TopSiteFile"
