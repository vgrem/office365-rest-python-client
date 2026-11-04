from __future__ import annotations

from office365.intune.devices.management.mobileapps.win32.returncodetype import (
    Win32LobAppReturnCodeType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Win32LobAppReturnCode(ClientValue):
    returnCode: int | None = None
    type: Win32LobAppReturnCodeType = Win32LobAppReturnCodeType.failed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Win32LobAppReturnCode"
