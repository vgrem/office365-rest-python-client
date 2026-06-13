from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from office365.onedrive.driveitems.source import DriveItemSource
from office365.onedrive.files.system_info import FileSystemInfo
from office365.onedrive.media_source import MediaSource
from office365.runtime.client_value import ClientValue
from office365.runtime.odata.json_format import ODataJsonFormat


@dataclass
class DriveItemUploadableProperties(ClientValue):
    """The driveItemUploadableProperties resource represents an item being uploaded when creating an upload session."""

    fileSystemInfo: FileSystemInfo | None = field(default_factory=FileSystemInfo)
    name: str | None = None
    description: str | None = None
    _fileSize: int | None = None
    driveItemSource: DriveItemSource = field(default_factory=DriveItemSource)
    fileSize: int | None = None
    mediaSource: MediaSource = field(default_factory=MediaSource)

    @property
    def file_size(self):
        """Provides an expected file size to perform a quota check prior to upload. Only on OneDrive Personal."""
        return self._fileSize

    def to_json(self, json_format: Optional[ODataJsonFormat] = None) -> Dict[str, Any]:
        payload =  super().to_json(json_format)
        payload.pop("driveItemSource", None)
        payload.pop("mediaSource", None)
        return payload

    @property
    def entity_type_name(self) -> str:
        return None # type: ignore
