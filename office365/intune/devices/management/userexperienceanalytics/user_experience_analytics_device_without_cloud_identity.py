from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsDeviceWithoutCloudIdentity(Entity):
    @odata(name="azureAdDeviceId")
    @property
    def azure_ad_device_id(self) -> Optional[str]:
        """Gets the azureAdDeviceId property"""
        return self.properties.get("azureAdDeviceId", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceWithoutCloudIdentity"
