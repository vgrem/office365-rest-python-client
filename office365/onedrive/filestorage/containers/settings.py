from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FileStorageContainerSettings(ClientValue):
    isItemVersioningEnabled: bool | None = None
    isOcrEnabled: bool | None = None
    itemMajorVersionLimit: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerSettings"
