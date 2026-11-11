from __future__ import annotations

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery


class WorkbookChartFill(Entity):
    """Represents the fill formatting for a chart element."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookChartFill"

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def clear(self) -> Self:
        """clear operation."""
        qry = ServiceOperationQuery(self, "clear", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(delegated=["Files.ReadWrite"], application=["Files.ReadWrite.All"])
    def set_solid_color(self, color: str) -> Self:
        """setSolidColor operation.

        Args:
            color (str):
                color parameter
        """
        qry = ServiceOperationQuery(self, "setSolidColor", None, {"color": color}, None, None)
        self.context.add_query(qry)
        return self
