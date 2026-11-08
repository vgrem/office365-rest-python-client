from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata
from office365.teams.viva.engagement.asyncoperationtype import EngagementAsyncOperationType


class EngagementAsyncOperation(PollableOperation, Entity):
    @odata(name="operationType")
    @property
    def operation_type(self) -> EngagementAsyncOperationType:
        """Gets the operationType property"""
        return self.properties.get("operationType", EngagementAsyncOperationType.createCommunity)

    @odata(name="resourceId")
    @property
    def resource_id(self) -> Optional[str]:
        """Gets the resourceId property"""
        return self.properties.get("resourceId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EngagementAsyncOperation"
