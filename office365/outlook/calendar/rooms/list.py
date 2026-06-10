from typing import Optional

from office365.entity_collection import EntityCollection
from office365.outlook.calendar.place import Place
from office365.outlook.calendar.rooms.room import Room
from office365.outlook.calendar.rooms.workspace import Workspace
from office365.runtime.paths.resource_path import ResourcePath


class RoomList(Place):
    """Represents a group of room objects defined in the tenant."""

    @property
    def email_address(self) -> Optional[str]:
        """The email address of the room list"""
        return self.properties.get("emailAddress", None)

    @property
    def rooms(self) -> EntityCollection[Room]:
        """The rooms in the room list. Navigation property. Read-only. Nullable."""
        return self.properties.get(
            "rooms",
            EntityCollection(self.context, Room, ResourcePath("rooms", self.resource_path)),
        )

    @property
    def workspaces(self) -> EntityCollection[Workspace]:
        """The workspaces in the room list. Navigation property. Read-only. Nullable."""
        return self.properties.get(
            "workspaces",
            EntityCollection(self.context, Workspace, ResourcePath("workspaces", self.resource_path)),
        )
