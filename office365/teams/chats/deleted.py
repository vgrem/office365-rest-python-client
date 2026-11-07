from __future__ import annotations

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery


class DeletedChat(Entity):
    """Represents a chat that was deleted in Microsoft Teams."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeletedChat"

    def undo_delete(self) -> Self:
        """undoDelete operation."""
        qry = ServiceOperationQuery(self, "undoDelete", None, {}, None, None)
        self.context.add_query(qry)
        return self
