from __future__ import annotations

from office365.intune.devices.management.windows_information_protection_app import WindowsInformationProtectionApp


class WindowsInformationProtectionDesktopApp(WindowsInformationProtectionApp):
    binaryName: str | None = None
    binaryVersionHigh: str | None = None
    binaryVersionLow: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionDesktopApp"
