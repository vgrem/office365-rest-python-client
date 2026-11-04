from __future__ import annotations

from office365.intune.devices.imported_windows_autopilot_device_identity_import_status import (
    ImportedWindowsAutopilotDeviceIdentityImportStatus,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ImportedWindowsAutopilotDeviceIdentityState(ClientValue):
    deviceErrorCode: int | None = None
    deviceErrorName: str | None = None
    deviceImportStatus: ImportedWindowsAutopilotDeviceIdentityImportStatus = (
        ImportedWindowsAutopilotDeviceIdentityImportStatus.unknown
    )
    deviceRegistrationId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ImportedWindowsAutopilotDeviceIdentityState"
