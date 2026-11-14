from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsNotAutopilotReadyDevice(Entity):
    @odata(name="autoPilotProfileAssigned")
    @property
    def auto_pilot_profile_assigned(self) -> Optional[bool]:
        """Gets the autoPilotProfileAssigned property"""
        return self.properties.get("autoPilotProfileAssigned", None)

    @odata(name="autoPilotRegistered")
    @property
    def auto_pilot_registered(self) -> Optional[bool]:
        """Gets the autoPilotRegistered property"""
        return self.properties.get("autoPilotRegistered", None)

    @odata(name="azureAdJoinType")
    @property
    def azure_ad_join_type(self) -> Optional[str]:
        """Gets the azureAdJoinType property"""
        return self.properties.get("azureAdJoinType", None)

    @odata(name="azureAdRegistered")
    @property
    def azure_ad_registered(self) -> Optional[bool]:
        """Gets the azureAdRegistered property"""
        return self.properties.get("azureAdRegistered", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="managedBy")
    @property
    def managed_by(self) -> Optional[str]:
        """Gets the managedBy property"""
        return self.properties.get("managedBy", None)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="serialNumber")
    @property
    def serial_number(self) -> Optional[str]:
        """Gets the serialNumber property"""
        return self.properties.get("serialNumber", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsNotAutopilotReadyDevice"
