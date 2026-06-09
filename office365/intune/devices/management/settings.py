from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DeviceManagementSettings(ClientValue):
    """intuneBrand contains data which is used in customizing the appearance of the Company Portal applications as
    well as the end user web portal.

    Args:
        device_compliance_checkin_threshold_days (int): The number of days a device is allowed to go without checking in to remain compliant.
        is_scheduled_action_enabled (bool): Is feature enabled or not for scheduled action for rule.
        secure_by_default (bool): Device should be noncompliant when there is no compliance policy targeted when this is true
    """

    deviceComplianceCheckinThresholdDays: int | None = None
    isScheduledActionEnabled: bool | None = None
    secureByDefault: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementSettings"
