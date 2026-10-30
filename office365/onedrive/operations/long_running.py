from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onedrive.operations.longrunningoperationstatus import (
        LongRunningOperationStatus,
    )


class LongRunningOperation(PollableOperation, Entity):
    """The status of a long-running operation."""

    @odata(name="resourceLocation")
    @property
    def resource_location(self) -> Optional[str]:
        """URI of the resource that the operation is performed on."""
        return self.properties.get("resourceLocation", None)

    @odata(name="statusDetail")
    @property
    def status_detail(self) -> Optional[str]:
        """Details about the status of the operation."""
        return self.properties.get("statusDetail", None)

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
    def status(self) -> LongRunningOperationStatus:
        """Gets the status property"""
        from office365.onedrive.operations.longrunningoperationstatus import (
            LongRunningOperationStatus,
        )

        return self.properties.get("status", LongRunningOperationStatus.notStarted)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LongRunningOperation"
