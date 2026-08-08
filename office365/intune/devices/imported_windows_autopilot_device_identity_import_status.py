from __future__ import annotations

from enum import Enum


class ImportedWindowsAutopilotDeviceIdentityImportStatus(Enum):
    unknown = "0"
    pending = "1"
    partial = "2"
    complete = "3"
    error = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ImportedWindowsAutopilotDeviceIdentityImportStatus"
