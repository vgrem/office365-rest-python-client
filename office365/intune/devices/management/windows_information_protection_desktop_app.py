from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WindowsInformationProtectionDesktopApp(ClientValue):
    binaryName: str | None = None
    binaryVersionHigh: str | None = None
    binaryVersionLow: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionDesktopApp"
