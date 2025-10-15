from typing import Optional

from office365.sharepoint.entity import Entity


class CanCreatePageResponse(Entity):

    @property
    def can_create_page(self) -> Optional[bool]:
        """Gets the CanCreatePage property"""
        return self.properties.get("CanCreatePage", None)

    @property
    def can_create_promoted_page(self) -> Optional[bool]:
        """Gets the CanCreatePromotedPage property"""
        return self.properties.get("CanCreatePromotedPage", None)

    @property
    def enable_moderation(self) -> Optional[bool]:
        """Gets the EnableModeration property"""
        return self.properties.get("EnableModeration", None)

    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.CanCreatePageResponse"
