from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileSystemInfo(ClientValue):
    """The FileSystemInfo resource contains properties that are reported by the device's local file system for the
    local version of an item."""

    createdDateTime: str | None = None
    lastAccessedDateTime: str | None = None
    lastModifiedDateTime: str | None = None
