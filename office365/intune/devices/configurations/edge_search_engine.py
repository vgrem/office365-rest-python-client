from __future__ import annotations

from office365.intune.devices.configurations.windows.general.edgesearchenginetype import (
    EdgeSearchEngineType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EdgeSearchEngine(ClientValue):
    edgeSearchEngineType: EdgeSearchEngineType = EdgeSearchEngineType.default

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EdgeSearchEngine"
