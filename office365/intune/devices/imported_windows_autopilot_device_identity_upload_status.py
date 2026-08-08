from __future__ import annotations

from enum import Enum


class ImportedWindowsAutopilotDeviceIdentityUploadStatus(Enum):
    noUpload = "0"
    pending = "1"
    complete = "2"
    error = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ImportedWindowsAutopilotDeviceIdentityUploadStatus"
