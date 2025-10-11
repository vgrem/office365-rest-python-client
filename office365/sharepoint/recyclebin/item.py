from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.principal.users.user import User
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


class RecycleBinItem(Entity):
    """Represents a Recycle Bin item in the Recycle Bin of a site or a site collection."""

    def __str__(self):
        return self.title or self.entity_type_name

    def restore(self) -> Self:
        """Restores the Recycle Bin item to its original location."""
        qry = ServiceOperationQuery(self, "Restore")
        self.context.add_query(qry)
        return self

    def move_to_second_stage(self) -> Self:
        """
        Moves the Recycle Bin item from the first-stage Recycle Bin to the second-stage Recycle Bin if the
        SecondStageRecycleBinQuota property on the current web application is not 0. Otherwise, deletes the item.
        """
        qry = ServiceOperationQuery(self, "MoveToSecondStage")
        self.context.add_query(qry)
        return self

    @property
    def author_email(self) -> Optional[str]:
        """Gets the email address of the user who originally created the Recycle Bin item."""
        return self.properties.get("AuthorEmail", None)

    @property
    def author_name(self) -> Optional[str]:
        """Gets the user display name of the user who originally created the Recycle Bin item."""
        return self.properties.get("AuthorName", None)

    @property
    def deleted_by_email(self) -> Optional[str]:
        """Gets the email address of the user who deleted the Recycle Bin item."""
        return self.properties.get("DeletedByEmail", None)

    @property
    def deleted_by_name(self) -> Optional[str]:
        """Gets the user display name of the user who deleted the Recycle Bin item."""
        return self.properties.get("DeletedByName", None)

    @property
    def deleted_date_local_formatted(self) -> Optional[str]:
        """
        Specifies when, in the default time zone for the current site,
        the Recycle Bin item was moved to the Recycle Bin.
        """
        return self.properties.get("DeletedDateLocalFormatted", None)

    @property
    def dir_name(self) -> Optional[str]:
        """
        Specifies the site-relative URL of the list or folder that originally contained the Recycle Bin item.
        """
        return self.properties.get("DirName", None)

    @property
    def dir_name_path(self) -> Optional[SPResPath]:
        """Returns the site relative path of the list or folder that originally contained the Recycle Bin item."""
        return self.properties.get("DirNamePath", SPResPath())

    @property
    def item_state(self) -> Optional[int]:
        """Specifies the Recycle Bin stage of the Recycle Bin item."""
        return self.properties.get("ItemState", None)

    @property
    def item_type(self) -> Optional[int]:
        """Specifies the type of the Recycle Bin item."""
        return self.properties.get("ItemType", None)

    @property
    def id(self) -> Optional[str]:
        """Gets a value that specifies the identifier of the Recycle Bin item."""
        return self.properties.get("Id", None)

    @property
    def leaf_name(self) -> Optional[str]:
        """Specifies the leaf name of the Recycle Bin item."""
        return self.properties.get("LeafName", None)

    @property
    def leaf_name_path(self) -> Optional[SPResPath]:
        """Returns the leaf name path of the Recycle Bin item."""
        return self.properties.get("LeafNamePath", SPResPath())

    @property
    def size(self) -> Optional[int]:
        """Gets a value that specifies the size of the Recycle Bin item in bytes."""
        return self.properties.get("Size", None)

    @property
    def title(self) -> Optional[str]:
        """Specifies the title of the Recycle Bin item."""
        return self.properties.get("Title", None)

    @property
    def author(self) -> User:
        """Gets a value that specifies the user who created the Recycle Bin item."""
        return self.properties.get("Author", User(self.context, ResourcePath("Author", self.resource_path)))

    @property
    def deleted_by(self) -> User:
        """Gets a value that specifies the user who deleted the Recycle Bin item."""
        return self.properties.get(
            "DeletedBy",
            User(self.context, ResourcePath("DeletedBy", self.resource_path)),
        )

    @property
    def deleted_date(self) -> datetime:
        """Gets a value that specifies when the Recycle Bin item was moved to the Recycle Bin."""
        return self.properties.get("DeletedDate", datetime.min)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "DeletedBy": self.deleted_by,
                "DeletedDate": self.deleted_date,
                "DirNamePath": self.dir_name_path,
                "LeafNamePath": self.leaf_name_path,
            }
            default_value = property_mapping.get(name, None)
        return super(RecycleBinItem, self).get_property(name, default_value)
