from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class WorkbookChartLineFormat(Entity):
    @odata(name="color")
    @property
    def color(self) -> Optional[str]:
        """Gets the color property"""
        return self.properties.get("color", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookChartLineFormat"

    def clear(self) -> Self:
        """clear operation."""
        qry = ServiceOperationQuery(self, "clear", None, {}, None, None)
        self.context.add_query(qry)
        return self
