from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsRemoteConnection(Entity):
    @odata(name="cloudPcFailurePercentage")
    @property
    def cloud_pc_failure_percentage(self) -> Optional[float]:
        """Gets the cloudPcFailurePercentage property"""
        return self.properties.get("cloudPcFailurePercentage", None)

    @odata(name="cloudPcRoundTripTime")
    @property
    def cloud_pc_round_trip_time(self) -> Optional[float]:
        """Gets the cloudPcRoundTripTime property"""
        return self.properties.get("cloudPcRoundTripTime", None)

    @odata(name="cloudPcSignInTime")
    @property
    def cloud_pc_sign_in_time(self) -> Optional[float]:
        """Gets the cloudPcSignInTime property"""
        return self.properties.get("cloudPcSignInTime", None)

    @odata(name="coreBootTime")
    @property
    def core_boot_time(self) -> Optional[float]:
        """Gets the coreBootTime property"""
        return self.properties.get("coreBootTime", None)

    @odata(name="coreSignInTime")
    @property
    def core_sign_in_time(self) -> Optional[float]:
        """Gets the coreSignInTime property"""
        return self.properties.get("coreSignInTime", None)

    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

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

    @odata(name="remoteSignInTime")
    @property
    def remote_sign_in_time(self) -> Optional[float]:
        """Gets the remoteSignInTime property"""
        return self.properties.get("remoteSignInTime", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @odata(name="virtualNetwork")
    @property
    def virtual_network(self) -> Optional[str]:
        """Gets the virtualNetwork property"""
        return self.properties.get("virtualNetwork", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsRemoteConnection"
