from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DeviceAndAppManagementData(ClientValue):
    """Exported Data"""

    content: bytes | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAndAppManagementData"
