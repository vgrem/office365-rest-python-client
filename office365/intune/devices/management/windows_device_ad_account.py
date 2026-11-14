from __future__ import annotations

from office365.intune.devices.management.windows_device_account import WindowsDeviceAccount


class WindowsDeviceADAccount(WindowsDeviceAccount):
    domainName: str | None = None
    userName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDeviceADAccount"
