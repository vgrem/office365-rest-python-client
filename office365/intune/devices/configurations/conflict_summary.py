from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.setting_source import SettingSource
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceConfigurationConflictSummary(Entity):
    @odata(name="conflictingDeviceConfigurations")
    @property
    def conflicting_device_configurations(self) -> ClientValueCollection[SettingSource]:
        """Gets the conflictingDeviceConfigurations property"""
        return self.properties.get(
            "conflictingDeviceConfigurations", ClientValueCollection[SettingSource](SettingSource)
        )

    @odata(name="contributingSettings")
    @property
    def contributing_settings(self) -> StringCollection:
        """Gets the contributingSettings property"""
        return self.properties.get("contributingSettings", StringCollection())

    @odata(name="deviceCheckinsImpacted")
    @property
    def device_checkins_impacted(self) -> Optional[int]:
        """Gets the deviceCheckinsImpacted property"""
        return self.properties.get("deviceCheckinsImpacted", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceConfigurationConflictSummary"
