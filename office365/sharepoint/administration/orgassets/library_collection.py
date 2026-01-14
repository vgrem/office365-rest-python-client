from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.administration.orgassets.library import OrgAssetsLibrary


class OrgAssetsLibraryCollection(ClientValue):
    def __init__(
        self,
        org_assets_libraries: ClientValueCollection[OrgAssetsLibrary] = ClientValueCollection(OrgAssetsLibrary),
        items: ClientValueCollection[OrgAssetsLibrary] = ClientValueCollection(OrgAssetsLibrary),
    ):
        self.OrgAssetsLibraries = org_assets_libraries
        self.Items = items

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssetsLibraryCollection"
