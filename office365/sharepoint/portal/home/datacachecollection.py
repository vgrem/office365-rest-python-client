from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.home.datacache import SharePointHomeDataCache


class SharePointHomeDataCacheCollection(ClientValue):
    def __init__(
        self,
        items: ClientValueCollection[SharePointHomeDataCache] = ClientValueCollection(SharePointHomeDataCache),
    ):
        self.Items = items

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomeDataCacheCollection"
