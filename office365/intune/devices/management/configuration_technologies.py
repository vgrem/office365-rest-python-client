from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationTechnologies(Enum):
    none = "0"
    mdm = "1"
    windows10XManagement = "2"
    configManager = "4"
    intuneManagementExtension = "8"
    thirdParty = "16"
    documentGateway = "32"
    appleRemoteManagement = "64"
    microsoftSense = "128"
    exchangeOnline = "256"
    mobileApplicationManagement = "512"
    linuxMdm = "1024"
    enrollment = "4096"
    endpointPrivilegeManagement = "8192"
    unknownFutureValue = "16384"
    windowsOsRecovery = "32768"
    android = "65536"
    intuneOpenExtensibility = "131072"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationTechnologies"
