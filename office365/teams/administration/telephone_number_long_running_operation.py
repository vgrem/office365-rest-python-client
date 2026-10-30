from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.onedrive.operations.longrunningoperationstatus import (
    LongRunningOperationStatus,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.teams.telephone_number_long_running_operation_details import (
        TelephoneNumberLongRunningOperationDetails,
    )


class TelephoneNumberLongRunningOperation(PollableOperation, Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[str]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="status")
    @property
    def status(self) -> LongRunningOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", LongRunningOperationStatus.notStarted)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TelephoneNumberLongRunningOperation"

    @odata(name="numbers")
    @property
    def numbers(self) -> ClientValueCollection[TelephoneNumberLongRunningOperationDetails]:
        """Gets the numbers property"""
        from office365.teams.telephone_number_long_running_operation_details import (
            TelephoneNumberLongRunningOperationDetails,
        )

        return self.properties.get(
            "numbers",
            ClientValueCollection[TelephoneNumberLongRunningOperationDetails](
                TelephoneNumberLongRunningOperationDetails
            ),
        )
