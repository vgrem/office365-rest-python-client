from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.authentication.methods.keystrength import AuthenticationMethodKeyStrength
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.device import Device


class WindowsHelloForBusinessAuthenticationMethod(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="keyStrength")
    @property
    def key_strength(self) -> AuthenticationMethodKeyStrength:
        """Gets the keyStrength property"""
        return self.properties.get("keyStrength", AuthenticationMethodKeyStrength.normal)

    @odata(name="device", navigation=True)
    @property
    def device(self) -> Device:
        """Gets the device property"""
        from office365.intune.devices.device import Device

        return self.properties.get("device", Device(self.context, ResourcePath("device", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsHelloForBusinessAuthenticationMethod"
