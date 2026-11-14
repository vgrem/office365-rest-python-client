from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationTemplateFamily(Enum):
    none = "0"
    endpointSecurityAntivirus = "10"
    endpointSecurityDiskEncryption = "11"
    endpointSecurityFirewall = "12"
    endpointSecurityEndpointDetectionAndResponse = "13"
    endpointSecurityAttackSurfaceReduction = "14"
    endpointSecurityAccountProtection = "15"
    endpointSecurityApplicationControl = "16"
    endpointSecurityEndpointPrivilegeManagement = "17"
    enrollmentConfiguration = "18"
    appQuietTime = "19"
    baseline = "20"
    unknownFutureValue = "21"
    deviceConfigurationScripts = "22"
    deviceConfigurationPolicies = "23"
    windowsOsRecoveryPolicies = "24"
    companyPortal = "25"
    windowsRecoveryAndRemediationConfiguration = "26"
    maintenanceWindows = "27"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationTemplateFamily"
