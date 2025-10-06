from office365.runtime.client_value import ClientValue


class SPSiteCollectionScopedPermissionInfo(ClientValue):

    def __init__(
        self,
        list_id: str = None,
        right: str = None,
        site_id: str = None,
        web_id: str = None,
    ):
        self.listId = list_id
        self.right = right
        self.siteId = site_id
        self.webId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPSiteCollectionScopedPermissionInfo"
