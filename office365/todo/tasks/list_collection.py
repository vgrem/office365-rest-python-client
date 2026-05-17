from office365.delta_collection import DeltaCollection
from office365.todo.tasks.list import TodoTaskList


class TodoTaskListCollection(DeltaCollection[TodoTaskList]):
    """ """

    def __init__(self, context, resource_path=None):
        super().__init__(context, TodoTaskList, resource_path)

    def add(self, display_name: str) -> TodoTaskList:
        """
        Create a new lists object.

        :param str display_name: Field indicating title of the task list.
        """
        return super().add(displayName=display_name)
