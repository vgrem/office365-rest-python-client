from __future__ import annotations

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.verbs import verb


class DeletedChat(Entity):
    """Represents a chat that was deleted in Microsoft Teams."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeletedChat"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["Chat.ManageDeletion.All"],
        application=["Chat.ManageDeletion.All"],
    )
    def undo_delete(self) -> Self:
        """undoDelete operation."""
        qry = ServiceOperationQuery(self, "undoDelete", None, {}, None, None)
        self.context.add_query(qry)
        return self
