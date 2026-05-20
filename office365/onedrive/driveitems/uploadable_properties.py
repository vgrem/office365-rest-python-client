from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.files.system_info import FileSystemInfo
from office365.runtime.client_value import ClientValue


@dataclass
class DriveItemUploadableProperties(ClientValue):
    """The driveItemUploadableProperties resource represents an item being uploaded when creating an upload session."""

    fileSystemInfo: FileSystemInfo | None = field(default_factory=FileSystemInfo)
    name: str | None = None
    description: str | None = None
    _fileSize: int | None = None

    @property
    def file_size(self):
        """Provides an expected file size to perform a quota check prior to upload. Only on OneDrive Personal."""
        return self._fileSize
