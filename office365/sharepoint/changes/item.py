from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.changes.change import Change
from office365.sharepoint.contenttypes.content_type_id import ContentTypeId
from office365.sharepoint.sharing.shared_with_user import SharedWithUser


class ChangeItem(Change):
    """A change on an item."""

    @odata(name="ActivityType", beta=True)
    @property
    def activity_type(self) -> Optional[str]:
        """Returns activity type defined in ChangeActivityType"""
        return self.properties.get("ActivityType", None)

    @odata(name="ContentTypeId", beta=True)
    @property
    def content_type_id(self) -> ContentTypeId:
        """Specifies an identifier for the content type"""
        return self.properties.get("ContentTypeId", ContentTypeId())

    @odata(name="Editor")
    @property
    def editor(self) -> Optional[str]:
        """Specifies the editor of the changed item."""
        return self.properties.get("Editor", None)

    @odata(name="EditorEmailHint")
    @property
    def editor_email_hint(self) -> Optional[str]:
        """Returns the email corresponding to Editor."""
        return self.properties.get("EditorEmailHint", None)

    @odata(name="EditorLoginName", beta=True)
    @property
    def editor_login_name(self) -> Optional[str]:
        """Returns login name of the Editor."""
        return self.properties.get("EditorLoginName", None)

    @odata(name="FileType", beta=True)
    @property
    def file_type(self) -> Optional[str]:
        """Returns the list item’s file type."""
        return self.properties.get("FileType", None)

    @odata(name="ItemId")
    @property
    def item_id(self) -> Optional[int]:
        """Identifies the changed item."""
        return self.properties.get("ItemId", None)

    @odata(name="IsRecycleBinOperation", beta=True)
    @property
    def is_recycle_bin_operation(self) -> Optional[bool]:
        return self.properties.get("IsRecycleBinOperation", None)

    @odata(name="ServerRelativeUrl")
    @property
    def server_relative_url(self) -> Optional[str]:
        """Specifies the server-relative URL of the item."""
        return self.properties.get("ServerRelativeUrl", None)

    @odata(name="SharedByUser")
    @property
    def shared_by_user(self) -> SharedWithUser:
        """Return the sharedBy User Information in sharing action for change log."""
        return self.properties.get("SharedByUser", SharedWithUser())

    @odata(name="SharedWithUsers")
    @property
    def shared_with_users(self) -> ClientValueCollection[SharedWithUser]:
        """Returns the array of users that have been shared in sharing action for the change log."""
        return self.properties.get("SharedWithUsers", ClientValueCollection(SharedWithUser))

    @odata(name="UniqueId")
    @property
    def unique_id(self) -> Optional[str]:
        """The Document identifier of the item."""
        return self.properties.get("UniqueId", None)

    @odata(name="FileSystemObjectType", beta=True)
    @property
    def file_system_object_type(self) -> Optional[int]:
        """Gets the FileSystemObjectType property"""
        return self.properties.get("FileSystemObjectType", None)

    @odata(name="Hashtag", beta=True)
    @property
    def hashtag(self) -> Optional[str]:
        """Gets the Hashtag property"""
        return self.properties.get("Hashtag", None)

    @odata(name="Hidden", beta=True)
    @property
    def hidden(self) -> Optional[bool]:
        """Gets the Hidden property"""
        return self.properties.get("Hidden", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the ListId property"""
        return self.properties.get("ListId", None)

    @odata(name="ListTemplate", beta=True)
    @property
    def list_template(self) -> Optional[int]:
        """Gets the ListTemplate property"""
        return self.properties.get("ListTemplate", None)

    @odata(name="ListTitle", beta=True)
    @property
    def list_title(self) -> Optional[str]:
        """Gets the ListTitle property"""
        return self.properties.get("ListTitle", None)

    @odata(name="MoveWasForRecycle", beta=True)
    @property
    def move_was_for_recycle(self) -> Optional[bool]:
        """Gets the MoveWasForRecycle property"""
        return self.properties.get("MoveWasForRecycle", None)

    @odata(name="MoveWasForRestore", beta=True)
    @property
    def move_was_for_restore(self) -> Optional[bool]:
        """Gets the MoveWasForRestore property"""
        return self.properties.get("MoveWasForRestore", None)

    @odata(name="Title", beta=True)
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)
