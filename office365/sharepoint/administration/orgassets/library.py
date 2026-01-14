from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


class OrgAssetsLibrary(ClientValue):
    def __init__(
        self,
        display_name: str = None,
        file_type: str = None,
        library_url: ResourcePath = ResourcePath(),
        list_id: str = None,
        org_asset_flags: int = None,
        org_asset_type: int = None,
        thumbnail_url: ResourcePath = ResourcePath(),
        unique_id: str = None,
    ):
        self.DisplayName = display_name
        self.FileType = file_type
        self.LibraryUrl = library_url
        self.ListId = list_id
        self.OrgAssetFlags = org_asset_flags
        self.OrgAssetType = org_asset_type
        self.ThumbnailUrl = thumbnail_url
        self.UniqueId = unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssetsLibrary"
