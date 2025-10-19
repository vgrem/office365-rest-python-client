from datetime import datetime
from typing import Optional

from office365.sharepoint.directory.users.information import UserInformation
from office365.sharepoint.entity import Entity


class FileSystemItem(Entity):

    @property
    def created_by(self) -> UserInformation:
        """Gets the CreatedBy property"""
        return self.properties.get("CreatedBy", UserInformation())

    @property
    def e_tag(self) -> Optional[str]:
        """Gets the ETag property"""
        return self.properties.get("ETag", None)

    @property
    def last_modified_by(self) -> UserInformation:
        """Gets the LastModifiedBy property"""
        return self.properties.get("LastModifiedBy", UserInformation())

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def size(self) -> Optional[int]:
        """Gets the Size property"""
        return self.properties.get("Size", None)

    @property
    def time_created(self) -> datetime:
        """Gets the TimeCreated property"""
        return self.properties.get("TimeCreated", datetime.min)

    @property
    def time_last_modified(self) -> datetime:
        """Gets the TimeLastModified property"""
        return self.properties.get("TimeLastModified", datetime.min)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "MS.FileServices.FileSystemItem"
