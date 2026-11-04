from __future__ import annotations

from office365.directory.synchronization.metadata import SynchronizationMetadata
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SynchronizationMetadataEntry(ClientValue):
    key: SynchronizationMetadata = SynchronizationMetadata.GalleryApplicationIdentifier
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationMetadataEntry"
