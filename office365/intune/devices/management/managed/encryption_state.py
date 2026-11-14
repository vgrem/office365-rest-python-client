from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.status import ComplianceStatus
from office365.runtime.types.odata_property import odata, version


@version("beta")
class ManagedDeviceEncryptionState(Entity):
    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="encryptionPolicySettingState")
    @property
    def encryption_policy_setting_state(self) -> ComplianceStatus:
        """Gets the encryptionPolicySettingState property"""
        return self.properties.get("encryptionPolicySettingState", ComplianceStatus.unknown)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="tpmSpecificationVersion")
    @property
    def tpm_specification_version(self) -> Optional[str]:
        """Gets the tpmSpecificationVersion property"""
        return self.properties.get("tpmSpecificationVersion", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedDeviceEncryptionState"
