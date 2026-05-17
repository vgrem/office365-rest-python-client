from enum import Enum


class DevicePlatformType(Enum):
    android = "0"
    androidForWork = "1"
    iOS = "2"
    macOS = "3"
    windowsPhone81 = "4"
    windows81AndLater = "5"
    windows10AndLater = "6"
    androidWorkProfile = "7"
    unknown = "8"
    androidAOSP = "9"
    androidMobileApplicationManagement = "10"
    iOSMobileApplicationManagement = "11"
    unknownFutureValue = "12"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DevicePlatformType"
