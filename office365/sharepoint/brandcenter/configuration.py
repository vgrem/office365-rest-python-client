from office365.runtime.client_value import ClientValue
from office365.sharepoint.administration.orgassets.org_assets import OrgAssets
from office365.sharepoint.types.resource_path import ResourcePath


class BrandCenterConfiguration(ClientValue):

    def __init__(
        self,
        brand_colors_list_id: str = None,
        brand_colors_list_url: ResourcePath = ResourcePath(),
        brand_font_library_id: str = None,
        brand_font_library_url: ResourcePath = ResourcePath(),
        is_brand_center_site_feature_enabled: bool = None,
        is_public_cdn_enabled: bool = None,
        org_assets: OrgAssets = OrgAssets(),
        site_id: str = None,
        site_url: str = None,
    ):
        self.BrandColorsListId = brand_colors_list_id
        self.BrandColorsListUrl = brand_colors_list_url
        self.BrandFontLibraryId = brand_font_library_id
        self.BrandFontLibraryUrl = brand_font_library_url
        self.IsBrandCenterSiteFeatureEnabled = is_brand_center_site_feature_enabled
        self.IsPublicCdnEnabled = is_public_cdn_enabled
        self.OrgAssets = org_assets
        self.SiteId = site_id
        self.SiteUrl = site_url
