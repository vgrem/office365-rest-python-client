from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DeviceManagementSettings(ClientValue):
    """intuneBrand contains data which is used in customizing the appearance of the Company Portal applications as
    well as the end user web portal.

    Args:
        deviceComplianceCheckinThresholdDays (int): The number of days a device is allowed to go without checking
          in to remain compliant.
        isScheduledActionEnabled (bool): Is feature enabled or not for scheduled action for rule.
        secureByDefault (bool): Device should be noncompliant when there is no compliance policy targeted when
          this is true
    """

    deviceComplianceCheckinThresholdDays: int | None = None
    isScheduledActionEnabled: bool | None = None
    secureByDefault: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementSettings"
