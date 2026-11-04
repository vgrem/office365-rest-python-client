from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPSiteCollectionScopedPermissionInfo(ClientValue):
    listId: Optional[str] = None
    right: Optional[str] = None
    siteId: Optional[str] = None
    webId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPSiteCollectionScopedPermissionInfo"
