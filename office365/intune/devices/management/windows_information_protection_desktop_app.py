from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WindowsInformationProtectionDesktopApp(ClientValue):
    binaryName: str | None = None
    binaryVersionHigh: str | None = None
    binaryVersionLow: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionDesktopApp"
