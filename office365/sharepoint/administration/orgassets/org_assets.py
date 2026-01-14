from office365.runtime.client_value import ClientValue
from office365.sharepoint.administration.orgassets.library_collection import (
    OrgAssetsLibraryCollection,
)
from office365.sharepoint.types.resource_path import ResourcePath


class OrgAssets(ClientValue):
    def __init__(
        self,
        central_asset_repository_libraries: OrgAssetsLibraryCollection = OrgAssetsLibraryCollection(),
        domain: ResourcePath = ResourcePath(),
        org_assets_libraries: OrgAssetsLibraryCollection = OrgAssetsLibraryCollection(),
        site_id: str = None,
        url: ResourcePath = ResourcePath(),
        web_id: str = None,
    ):
        self.OrgAssetsLibraries = OrgAssetsLibraryCollection()
        self.CentralAssetRepositoryLibraries = central_asset_repository_libraries
        self.Domain = domain
        self.OrgAssetsLibraries = org_assets_libraries
        self.SiteId = site_id
        self.Url = url
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssets"
