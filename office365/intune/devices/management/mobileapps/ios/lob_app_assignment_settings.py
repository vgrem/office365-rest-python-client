from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IosLobAppAssignmentSettings(ClientValue):
    isRemovable: bool | None = None
    uninstallOnDeviceRemoval: bool | None = None
    vpnConfigurationId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosLobAppAssignmentSettings"
