from __future__ import annotations

from typing import Optional

from office365.planner.entity import PlannerEntity
from office365.planner.order_hints_by_assignee import PlannerOrderHintsByAssignee
from office365.runtime.types.odata_property import odata


class PlannerAssignedToTaskBoardTaskFormat(PlannerEntity):
    @odata(name="orderHintsByAssignee")
    @property
    def order_hints_by_assignee(self) -> PlannerOrderHintsByAssignee:
        """Gets the orderHintsByAssignee property"""
        return self.properties.get("orderHintsByAssignee", PlannerOrderHintsByAssignee())

    @odata(name="unassignedOrderHint")
    @property
    def unassigned_order_hint(self) -> Optional[str]:
        """Gets the unassignedOrderHint property"""
        return self.properties.get("unassignedOrderHint", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PlannerAssignedToTaskBoardTaskFormat"
