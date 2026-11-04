from __future__ import annotations

from office365.intune.devices.management.virtualendpoint.cloudpcs.restorepointfrequencytype import (
    CloudPcRestorePointFrequencyType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CloudPcRestorePointSetting(ClientValue):
    frequencyType: CloudPcRestorePointFrequencyType = CloudPcRestorePointFrequencyType.none
    userRestoreEnabled: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcRestorePointSetting"
