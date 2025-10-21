from enum import Enum


class ManagedDevicePartnerReportedHealthState(Enum):
    unknown = "0"
    activated = "1"
    deactivated = "2"
    secured = "3"
    lowSeverity = "4"
    mediumSeverity = "5"
    highSeverity = "6"
    unresponsive = "7"
    compromised = "8"
    misconfigured = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedDevicePartnerReportedHealthState"
