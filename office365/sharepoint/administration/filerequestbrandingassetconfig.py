from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.administration.filerequestbrandingprofile import FileRequestBrandingProfile


class FileRequestBrandingAssetConfig(ClientValue):
    def __init__(
        self,
        asset_library_relative_url: str = None,
        asset_library_url: str = None,
        branded_profiles: ClientValueCollection[FileRequestBrandingProfile] = ClientValueCollection(
            FileRequestBrandingProfile
        ),
    ):
        self.AssetLibraryRelativeUrl = asset_library_relative_url
        self.AssetLibraryUrl = asset_library_url
        self.BrandedProfiles = branded_profiles

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.FileRequestBrandingAssetConfig"
