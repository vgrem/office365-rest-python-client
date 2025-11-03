from enum import Enum


class WindowsDeviceHealthState(Enum):
    clean = "0"
    fullScanPending = "1"
    rebootPending = "2"
    manualStepsPending = "4"
    offlineScanPending = "8"
    critical = "16"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsDeviceHealthState"
