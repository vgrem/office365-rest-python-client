from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PointPublishingMagazineProps(Entity):
    @odata(name="BannerColor")
    @property
    def banner_color(self) -> Optional[str]:
        """Gets the BannerColor property"""
        return self.properties.get("BannerColor", None)

    @odata(name="BannerImageUrl")
    @property
    def banner_image_url(self) -> Optional[str]:
        """Gets the BannerImageUrl property"""
        return self.properties.get("BannerImageUrl", None)

    @odata(name="BannerPattern")
    @property
    def banner_pattern(self) -> Optional[str]:
        """Gets the BannerPattern property"""
        return self.properties.get("BannerPattern", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="IsUserContributor")
    @property
    def is_user_contributor(self) -> Optional[bool]:
        """Gets the IsUserContributor property"""
        return self.properties.get("IsUserContributor", None)

    @odata(name="IsUserOwner")
    @property
    def is_user_owner(self) -> Optional[bool]:
        """Gets the IsUserOwner property"""
        return self.properties.get("IsUserOwner", None)

    @odata(name="MagazineType")
    @property
    def magazine_type(self) -> Optional[int]:
        """Gets the MagazineType property"""
        return self.properties.get("MagazineType", None)

    @odata(name="PublishedDate")
    @property
    def published_date(self) -> Optional[datetime]:
        """Gets the PublishedDate property"""
        return self.properties.get("PublishedDate", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingMagazineProps"
