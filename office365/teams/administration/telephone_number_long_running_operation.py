from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.onedrive.operations.longrunningoperationstatus import LongRunningOperationStatus


class TelephoneNumberLongRunningOperation(Entity):
    @property
    def created_date_time(self) -> Optional[str]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @property
    def status(self) -> LongRunningOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", LongRunningOperationStatus.notStarted)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TelephoneNumberLongRunningOperation"
