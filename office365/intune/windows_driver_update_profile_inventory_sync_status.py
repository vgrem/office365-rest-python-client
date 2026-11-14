from __future__ import annotations

from datetime import datetime

from office365.intune.windows_driver_update_profile_inventory_sync_state import (
    WindowsDriverUpdateProfileInventorySyncState,
)
from office365.runtime.client_value import ClientValue


class WindowsDriverUpdateProfileInventorySyncStatus(ClientValue):
    driverInventorySyncState: WindowsDriverUpdateProfileInventorySyncState = (
        WindowsDriverUpdateProfileInventorySyncState.pending
    )
    lastSuccessfulSyncDateTime: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDriverUpdateProfileInventorySyncStatus"
