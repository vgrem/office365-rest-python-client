from __future__ import annotations

from office365.directory.identitygovernance.run import Run
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


class CancelRunsScope(ClientValue):
    runs: EntityCollection[Run] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.CancelRunsScope"
