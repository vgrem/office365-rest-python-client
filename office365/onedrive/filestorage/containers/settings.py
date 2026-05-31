from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileStorageContainerSettings(ClientValue):
    isItemVersioningEnabled: bool | None = None
    isOcrEnabled: bool | None = None
    itemMajorVersionLimit: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerSettings"
