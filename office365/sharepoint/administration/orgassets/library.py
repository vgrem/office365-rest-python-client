from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath
from typing import Optional


class OrgAssetsLibrary(ClientValue):
    def __init__(
        self,
        display_name: Optional[str] = None,
        file_type: Optional[str] = None,
        library_url: ResourcePath = ResourcePath(),
        list_id: Optional[str] = None,
        org_asset_flags: Optional[int] = None,
        org_asset_type: Optional[int] = None,
        thumbnail_url: ResourcePath = ResourcePath(),
        unique_id: Optional[str] = None,
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
