from __future__ import annotations

from dataclasses import field

from office365.directory.entity_type_and_ids import EntityTypeAndIds
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class RecoveryJobEntityNameAndIdsFilter(ClientValue):
    filterValues: ClientValueCollection[EntityTypeAndIds] = field(
        default_factory=lambda: ClientValueCollection(EntityTypeAndIds)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryJobEntityNameAndIdsFilter"
