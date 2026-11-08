from __future__ import annotations

from enum import Enum


class AssociatedAssignmentPayloadType(Enum):
    unknown = "0"
    deviceConfigurationAndCompliance = "1"
    application = "2"
    androidEnterpriseApp = "8"
    enrollmentConfiguration = "9"
    groupPolicyConfiguration = "12"
    zeroTouchDeploymentDeviceConfigProfile = "15"
    androidEnterpriseConfiguration = "16"
    deviceFirmwareConfigurationInterfacePolicy = "20"
    resourceAccessPolicy = "23"
    win32app = "24"
    deviceManagmentConfigurationAndCompliancePolicy = "29"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AssociatedAssignmentPayloadType"
