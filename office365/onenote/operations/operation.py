from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.onedrive.operations.longrunningoperationstatus import LongRunningOperationStatus


class Operation(Entity):
    """The status of a long-running operation."""

    @property
    def created_datetime(self) -> datetime:
        """
        The start time of the operation.
        """
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def last_action_date_time(self) -> Optional[datetime]:
        """Gets the lastActionDateTime property"""
        return self.properties.get("lastActionDateTime", datetime.min)

    @property
    def status(self) -> LongRunningOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", LongRunningOperationStatus.notStarted)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.Operation"
