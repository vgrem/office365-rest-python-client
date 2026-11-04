from __future__ import annotations

from office365.intune.devices.management.managed.windows.windows365_switch_compatibility_failure_reason_type import (
    Windows365SwitchCompatibilityFailureReasonType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CloudPcLaunchDetail(ClientValue):
    cloudPcId: str | None = None
    cloudPcLaunchUrl: str | None = None
    windows365SwitchCompatibilityFailureReasonType: Windows365SwitchCompatibilityFailureReasonType = (
        Windows365SwitchCompatibilityFailureReasonType.osVersionNotSupported
    )
    windows365SwitchCompatible: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcLaunchDetail"
