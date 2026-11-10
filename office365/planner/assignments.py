from __future__ import annotations

from typing import Any

from typing_extensions import Self

from office365.planner.assignment import PlannerAssignment
from office365.runtime.client_value import ClientValue
from office365.runtime.converters.value import deserialize_value


class PlannerAssignments(ClientValue):
    """The set of users assigned to a task.

    An Open Type serialized as a JSON object keyed by user id, where each value
    is a :class:`PlannerAssignment`.
    """

    _item_type = PlannerAssignment

    def set_property(self, name: str | int, value: Any, persist_changes: bool = True) -> Self:
        # Map raw JSON objects onto the typed assignment so reads stay strongly typed.
        if isinstance(value, dict):
            value = deserialize_value(self._item_type, value, None, persist_changes)
        return super().set_property(name, value, persist_changes)

    def add(self, user_id: str, *, order_hint: str = " !") -> str:
        """Assigns a user and returns their id.

        Args:
            user_id: The id of the user to assign.
            order_hint: Planner ordering hint; ``" !"`` appends.
        """
        user_id = str(user_id)
        self.set_property(user_id, PlannerAssignment(orderHint=order_hint))
        return user_id

    def remove(self, user_id: str) -> Self:
        """Unassigns a user.

        Graph drops the entry when its value is ``null``.
        """
        self.set_property(str(user_id), None)
        return self
