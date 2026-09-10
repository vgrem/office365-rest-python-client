from __future__ import annotations

from typing import Optional

from office365.directory.extensions.extension import Extension
from office365.directory.extensions.open_type import OpenTypeExtension
from office365.directory.permissions.require_permission import require_permission
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.todo.tasks.collection import TodoTaskCollection
from office365.todo.tasks.wellknownlistname import WellknownListName


class TodoTaskList(Entity):
    """A list in Microsoft To Do that contains one or more todoTask resources."""

    def __str__(self) -> str:
        return self.display_name or self.entity_type_name or ""

    @property
    def display_name(self) -> Optional[str]:
        """The name of the task list."""
        return self.properties.get("displayName", None)

    @property
    def is_owner(self) -> Optional[bool]:
        """Indicates whether the user is the owner of the task list."""
        return self.properties.get("isOwner", None)

    @property
    def is_shared(self) -> Optional[bool]:
        """Indicates whether the task list is shared with other users."""
        return self.properties.get("isShared", None)

    @property
    def wellknown_list_name(self) -> WellknownListName:
        """The name of the well-known list (``defaultList``/``flaggedEmails``/...)."""
        return self.properties.get("wellknownListName", WellknownListName.none)

    @property
    def extensions(self) -> EntityCollection[Extension]:
        """The collection of open extensions defined for the task list."""
        return self.properties.get(
            "extensions",
            EntityCollection(self.context, Extension, ResourcePath("extensions", self.resource_path)),
        )

    @require_permission(delegated=["Tasks.ReadWrite"])
    def add_extension(self, name: str, **properties) -> OpenTypeExtension:
        """Create an open type extension on the task list.

        Args:
            name (str): Unique text identifier (``extensionName``).
            **properties: Additional custom properties to store on the extension.
        """
        return_type = OpenTypeExtension(self.context)
        return_type.set_property("extensionName", name)
        for key, value in properties.items():
            return_type.set_property(key, value)
        self.extensions.add_child(return_type)
        qry = CreateEntityQuery(self.extensions, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def tasks(self) -> TodoTaskCollection:
        """The tasks in this task list."""
        return self.properties.get(
            "tasks",
            TodoTaskCollection(self.context, ResourcePath("tasks", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return None  # type: ignore
