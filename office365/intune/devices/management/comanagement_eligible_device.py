from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.agent_type import ManagementAgentType
from office365.intune.devices.management.managed.state import ManagementState
from office365.intune.devices.registrationstate import DeviceRegistrationState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class ComanagementEligibleDevice(Entity):
    @odata(name="clientRegistrationStatus")
    @property
    def client_registration_status(self) -> DeviceRegistrationState:
        """Gets the clientRegistrationStatus property"""
        return self.properties.get("clientRegistrationStatus", DeviceRegistrationState.notRegistered)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="entitySource")
    @property
    def entity_source(self) -> Optional[int]:
        """Gets the entitySource property"""
        return self.properties.get("entitySource", None)

    @odata(name="managementAgents")
    @property
    def management_agents(self) -> ManagementAgentType:
        """Gets the managementAgents property"""
        return self.properties.get("managementAgents", ManagementAgentType.eas)

    @odata(name="managementState")
    @property
    def management_state(self) -> ManagementState:
        """Gets the managementState property"""
        return self.properties.get("managementState", ManagementState.managed)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="mdmStatus")
    @property
    def mdm_status(self) -> Optional[str]:
        """Gets the mdmStatus property"""
        return self.properties.get("mdmStatus", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="osDescription")
    @property
    def os_description(self) -> Optional[str]:
        """Gets the osDescription property"""
        return self.properties.get("osDescription", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="referenceId")
    @property
    def reference_id(self) -> Optional[str]:
        """Gets the referenceId property"""
        return self.properties.get("referenceId", None)

    @odata(name="serialNumber")
    @property
    def serial_number(self) -> Optional[str]:
        """Gets the serialNumber property"""
        return self.properties.get("serialNumber", None)

    @odata(name="upn")
    @property
    def upn(self) -> Optional[str]:
        """Gets the upn property"""
        return self.properties.get("upn", None)

    @odata(name="userEmail")
    @property
    def user_email(self) -> Optional[str]:
        """Gets the userEmail property"""
        return self.properties.get("userEmail", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @odata(name="userName")
    @property
    def user_name(self) -> Optional[str]:
        """Gets the userName property"""
        return self.properties.get("userName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ComanagementEligibleDevice"
