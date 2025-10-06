from office365.runtime.client_value import ClientValue


class TopSiteFile(ClientValue):

    def __init__(
        self,
        content_type_id: str = None,
        list_id: str = None,
        source: int = None,
        unique_id: str = None,
    ):
        self.ContentTypeId = content_type_id
        self.ListId = list_id
        self.Source = source
        self.UniqueId = unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.TopSiteFile"
