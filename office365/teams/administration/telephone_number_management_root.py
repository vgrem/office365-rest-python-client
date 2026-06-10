from __future__ import annotations

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.teams.administration.telephone_number_long_running_operation import TelephoneNumberLongRunningOperation


class TelephoneNumberManagementRoot(Entity):
    @property
    def operations(self) -> EntityCollection[TelephoneNumberLongRunningOperation]:
        """Gets the operations property"""
        return self.properties.get(
            "operations",
            EntityCollection[TelephoneNumberLongRunningOperation](
                self.context, TelephoneNumberLongRunningOperation, ResourcePath("operations", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TelephoneNumberManagementRoot"
