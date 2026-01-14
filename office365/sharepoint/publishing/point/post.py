from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class PointPublishingPost(Entity):
    @property
    def author(self) -> Optional[str]:
        """Gets the Author property"""
        return self.properties.get("Author", None)

    @property
    def content(self) -> Optional[str]:
        """Gets the Content property"""
        return self.properties.get("Content", None)

    @property
    def created_date(self) -> datetime:
        """Gets the CreatedDate property"""
        return self.properties.get("CreatedDate", None)

    @property
    def friendly_url_file_name(self) -> Optional[str]:
        """Gets the FriendlyUrlFileName property"""
        return self.properties.get("FriendlyUrlFileName", None)

    @property
    def modified_date(self) -> datetime:
        """Gets the ModifiedDate property"""
        return self.properties.get("ModifiedDate", None)

    @property
    def operation_type(self) -> Optional[int]:
        """Gets the OperationType property"""
        return self.properties.get("OperationType", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def user_is_author(self) -> Optional[bool]:
        """Gets the UserIsAuthor property"""
        return self.properties.get("UserIsAuthor", None)

    @property
    def version(self) -> Optional[str]:
        """Gets the Version property"""
        return self.properties.get("Version", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingPost"
