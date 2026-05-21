from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DeviceManagementSettings(ClientValue):
    """intuneBrand contains data which is used in customizing the appearance of the Company Portal applications as
    well as the end user web portal.

    :param int device_compliance_checkin_threshold_days: The number of days a device is allowed to go without
        checking in to remain compliant.
    :param bool is_scheduled_action_enabled: Is feature enabled or not for scheduled action for rule.
    :param bool secure_by_default: Device should be noncompliant when there is no compliance policy targeted when
        this is true
    """

    deviceComplianceCheckinThresholdDays: int | None = None
    isScheduledActionEnabled: bool | None = None
    secureByDefault: bool | None = None
