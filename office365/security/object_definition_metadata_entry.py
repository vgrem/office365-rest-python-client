from __future__ import annotations

from office365.directory.synchronization.objectdefinitionmetadata import ObjectDefinitionMetadata
from office365.runtime.client_value import ClientValue


class ObjectDefinitionMetadataEntry(ClientValue):
    key: ObjectDefinitionMetadata = ObjectDefinitionMetadata.PropertyNameAccountEnabled
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ObjectDefinitionMetadataEntry"
