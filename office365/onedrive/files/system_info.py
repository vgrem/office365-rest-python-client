from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FileSystemInfo(ClientValue):
    """The FileSystemInfo resource contains properties that are reported by the device's local file system for the
    local version of an item."""

    createdDateTime: str | None = None
    lastAccessedDateTime: str | None = None
    lastModifiedDateTime: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileSystemInfo"
