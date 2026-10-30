from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.operationstatus import OperationStatus


class Operation(PollableOperation, Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastActionDateTime")
    @property
    def last_action_date_time(self) -> Optional[datetime]:
        """Gets the lastActionDateTime property"""
        return self.properties.get("lastActionDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> OperationStatus:
        """Gets the status property"""
        from office365.directory.identitygovernance.operationstatus import (
            OperationStatus,
        )

        return self.properties.get("status", OperationStatus.NotStarted)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Operation"
