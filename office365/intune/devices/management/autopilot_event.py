from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.intune.devices.enrollment.state import EnrollmentState
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from datetime import timedelta


@version("beta")
class DeviceManagementAutopilotEvent(Entity):
    @odata(name="accountSetupDuration")
    @property
    def account_setup_duration(self) -> Optional[timedelta]:
        """Gets the accountSetupDuration property"""
        return self.properties.get("accountSetupDuration", None)

    @odata(name="deploymentDuration")
    @property
    def deployment_duration(self) -> Optional[timedelta]:
        """Gets the deploymentDuration property"""
        return self.properties.get("deploymentDuration", None)

    @odata(name="deploymentEndDateTime")
    @property
    def deployment_end_date_time(self) -> Optional[datetime]:
        """Gets the deploymentEndDateTime property"""
        return self.properties.get("deploymentEndDateTime", None)

    @odata(name="deploymentStartDateTime")
    @property
    def deployment_start_date_time(self) -> Optional[datetime]:
        """Gets the deploymentStartDateTime property"""
        return self.properties.get("deploymentStartDateTime", None)

    @odata(name="deploymentTotalDuration")
    @property
    def deployment_total_duration(self) -> Optional[timedelta]:
        """Gets the deploymentTotalDuration property"""
        return self.properties.get("deploymentTotalDuration", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceRegisteredDateTime")
    @property
    def device_registered_date_time(self) -> Optional[datetime]:
        """Gets the deviceRegisteredDateTime property"""
        return self.properties.get("deviceRegisteredDateTime", None)

    @odata(name="deviceSerialNumber")
    @property
    def device_serial_number(self) -> Optional[str]:
        """Gets the deviceSerialNumber property"""
        return self.properties.get("deviceSerialNumber", None)

    @odata(name="deviceSetupDuration")
    @property
    def device_setup_duration(self) -> Optional[timedelta]:
        """Gets the deviceSetupDuration property"""
        return self.properties.get("deviceSetupDuration", None)

    @odata(name="enrollmentFailureDetails")
    @property
    def enrollment_failure_details(self) -> Optional[str]:
        """Gets the enrollmentFailureDetails property"""
        return self.properties.get("enrollmentFailureDetails", None)

    @odata(name="enrollmentStartDateTime")
    @property
    def enrollment_start_date_time(self) -> Optional[datetime]:
        """Gets the enrollmentStartDateTime property"""
        return self.properties.get("enrollmentStartDateTime", None)

    @odata(name="enrollmentState")
    @property
    def enrollment_state(self) -> EnrollmentState:
        """Gets the enrollmentState property"""
        return self.properties.get("enrollmentState", EnrollmentState.unknown)

    @odata(name="eventDateTime")
    @property
    def event_date_time(self) -> Optional[datetime]:
        """Gets the eventDateTime property"""
        return self.properties.get("eventDateTime", None)

    @odata(name="managedDeviceName")
    @property
    def managed_device_name(self) -> Optional[str]:
        """Gets the managedDeviceName property"""
        return self.properties.get("managedDeviceName", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @odata(name="windows10EnrollmentCompletionPageConfigurationDisplayName")
    @property
    def windows10_enrollment_completion_page_configuration_display_name(self) -> Optional[str]:
        """Gets the windows10EnrollmentCompletionPageConfigurationDisplayName property"""
        return self.properties.get("windows10EnrollmentCompletionPageConfigurationDisplayName", None)

    @odata(name="windows10EnrollmentCompletionPageConfigurationId")
    @property
    def windows10_enrollment_completion_page_configuration_id(self) -> Optional[str]:
        """Gets the windows10EnrollmentCompletionPageConfigurationId property"""
        return self.properties.get("windows10EnrollmentCompletionPageConfigurationId", None)

    @odata(name="windowsAutopilotDeploymentProfileDisplayName")
    @property
    def windows_autopilot_deployment_profile_display_name(self) -> Optional[str]:
        """Gets the windowsAutopilotDeploymentProfileDisplayName property"""
        return self.properties.get("windowsAutopilotDeploymentProfileDisplayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementAutopilotEvent"
