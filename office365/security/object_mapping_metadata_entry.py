from __future__ import annotations

from office365.directory.synchronization.objectmappingmetadata import ObjectMappingMetadata
from office365.runtime.client_value import ClientValue


class ObjectMappingMetadataEntry(ClientValue):
    key: ObjectMappingMetadata = ObjectMappingMetadata.EscrowBehavior
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ObjectMappingMetadataEntry"
