from __future__ import annotations

from office365.admin.microsoft365.appsupdatechanneltype import AppsUpdateChannelType
from office365.entity import Entity
from office365.intune.devices.management.mobileapps.apps_installation_options_for_mac import (  # noqa: E501
    AppsInstallationOptionsForMac,
)
from office365.intune.devices.management.mobileapps.apps_installation_options_for_windows import (  # noqa: E501
    AppsInstallationOptionsForWindows,
)
from office365.runtime.types.odata_property import odata


class M365AppsInstallationOptions(Entity):
    @odata(name="appsForMac")
    @property
    def apps_for_mac(self) -> AppsInstallationOptionsForMac:
        """Gets the appsForMac property"""
        return self.properties.get("appsForMac", AppsInstallationOptionsForMac())

    @odata(name="appsForWindows")
    @property
    def apps_for_windows(self) -> AppsInstallationOptionsForWindows:
        """Gets the appsForWindows property"""
        return self.properties.get("appsForWindows", AppsInstallationOptionsForWindows())

    @odata(name="updateChannel")
    @property
    def update_channel(self) -> AppsUpdateChannelType:
        """Gets the updateChannel property"""
        return self.properties.get("updateChannel", AppsUpdateChannelType.current)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.M365AppsInstallationOptions"
