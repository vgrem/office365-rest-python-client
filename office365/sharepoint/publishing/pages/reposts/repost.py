from typing import Optional

from office365.sharepoint.publishing.pages.page import SitePage


class RepostPage(SitePage):
    """Represents a re-posting of existing content where existing content can be a link to a resource on the
    internet or other page in your SharePoint environment"""

    @property
    def is_banner_image_url_external(self) -> Optional[bool]:
        return self.properties.get("IsBannerImageUrlExternal", None)

    @property
    def original_source_item_id(self) -> Optional[str]:
        return self.properties.get("OriginalSourceItemId", None)

    @property
    def original_source_url(self) -> Optional[str]:
        return self.properties.get("OriginalSourceUrl", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.RepostPage"
