from datetime import datetime
from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.files.file import File


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
    def created_date(self) -> Optional[datetime]:
        """Gets the CreatedDate property"""
        return self.properties.get("CreatedDate", None)

    @property
    def friendly_url_file_name(self) -> Optional[str]:
        """Gets the FriendlyUrlFileName property"""
        return self.properties.get("FriendlyUrlFileName", None)

    @property
    def modified_date(self) -> Optional[datetime]:
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

    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @property
    def images(self) -> EntityCollection[File]:
        """Gets the images property"""
        return self.properties.get(
            "images", EntityCollection[File](self.context, File, ResourcePath("images", self.resource_path))
        )

    def add_image_from_url(self, from_image_url: str) -> ClientResult[str]:
        """AddImageFromUrl operation.

        Args:
            from_image_url (str): fromImageUrl parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "AddImageFromUrl", None, {"fromImageUrl": from_image_url}, None, return_type)
        self.context.add_query(qry)
        return return_type
