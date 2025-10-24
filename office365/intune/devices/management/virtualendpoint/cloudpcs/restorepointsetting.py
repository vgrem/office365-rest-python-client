from office365.intune.devices.management.virtualendpoint.cloudpcs.restorepointfrequencytype import (
    CloudPcRestorePointFrequencyType,
)
from office365.runtime.client_value import ClientValue


class CloudPcRestorePointSetting(ClientValue):

    def __init__(
        self,
        frequency_type: CloudPcRestorePointFrequencyType = CloudPcRestorePointFrequencyType.none,
        user_restore_enabled: bool = None,
    ):
        self.frequencyType = frequency_type
        self.userRestoreEnabled = user_restore_enabled

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcRestorePointSetting"
