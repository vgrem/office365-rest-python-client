from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class PointPublishingMagazineProps(Entity):
    @property
    def banner_color(self) -> Optional[str]:
        """Gets the BannerColor property"""
        return self.properties.get("BannerColor", None)

    @property
    def banner_image_url(self) -> Optional[str]:
        """Gets the BannerImageUrl property"""
        return self.properties.get("BannerImageUrl", None)

    @property
    def banner_pattern(self) -> Optional[str]:
        """Gets the BannerPattern property"""
        return self.properties.get("BannerPattern", None)

    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @property
    def is_user_contributor(self) -> Optional[bool]:
        """Gets the IsUserContributor property"""
        return self.properties.get("IsUserContributor", None)

    @property
    def is_user_owner(self) -> Optional[bool]:
        """Gets the IsUserOwner property"""
        return self.properties.get("IsUserOwner", None)

    @property
    def magazine_type(self) -> Optional[int]:
        """Gets the MagazineType property"""
        return self.properties.get("MagazineType", None)

    @property
    def published_date(self) -> datetime:
        """Gets the PublishedDate property"""
        return self.properties.get("PublishedDate", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingMagazineProps"
