from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.todo.tasks.lists.collection import TodoTaskListCollection


class Todo(Entity):
    """Represents the To Do services available to a user."""

    @odata(name="lists", navigation=True)
    @property
    def lists(self) -> TodoTaskListCollection:
        """The task lists in the users mailbox."""
        return self.properties.get(
            "lists", TodoTaskListCollection(self.context, ResourcePath("lists", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Todo"
