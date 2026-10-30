from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.imported_windows_autopilot_device_identity_state import (
        ImportedWindowsAutopilotDeviceIdentityState,
    )


class ImportedWindowsAutopilotDeviceIdentity(Entity):
    @odata(name="assignedUserPrincipalName")
    @property
    def assigned_user_principal_name(self) -> Optional[str]:
        """Gets the assignedUserPrincipalName property"""
        return self.properties.get("assignedUserPrincipalName", None)

    @odata(name="groupTag")
    @property
    def group_tag(self) -> Optional[str]:
        """Gets the groupTag property"""
        return self.properties.get("groupTag", None)

    @odata(name="hardwareIdentifier")
    @property
    def hardware_identifier(self) -> Optional[bytes]:
        """Gets the hardwareIdentifier property"""
        return self.properties.get("hardwareIdentifier", None)

    @odata(name="importId")
    @property
    def import_id(self) -> Optional[str]:
        """Gets the importId property"""
        return self.properties.get("importId", None)

    @odata(name="productKey")
    @property
    def product_key(self) -> Optional[str]:
        """Gets the productKey property"""
        return self.properties.get("productKey", None)

    @odata(name="serialNumber")
    @property
    def serial_number(self) -> Optional[str]:
        """Gets the serialNumber property"""
        return self.properties.get("serialNumber", None)

    @odata(name="state")
    @property
    def state(self) -> ImportedWindowsAutopilotDeviceIdentityState:
        """Gets the state property"""
        from office365.intune.devices.management.imported_windows_autopilot_device_identity_state import (
            ImportedWindowsAutopilotDeviceIdentityState,
        )

        return self.properties.get("state", ImportedWindowsAutopilotDeviceIdentityState())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ImportedWindowsAutopilotDeviceIdentity"
