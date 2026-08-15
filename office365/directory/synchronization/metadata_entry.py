from __future__ import annotations

from dataclasses import dataclass

from office365.directory.synchronization.metadata import SynchronizationMetadata
from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationMetadataEntry(ClientValue):
    key: SynchronizationMetadata = SynchronizationMetadata.GalleryApplicationIdentifier
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationMetadataEntry"
