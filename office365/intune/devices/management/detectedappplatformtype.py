from enum import Enum


class DetectedAppPlatformType(Enum):
    unknown = "0"
    windows = "1"
    windowsMobile = "2"
    windowsHolographic = "3"
    ios = "4"
    macOS = "5"
    chromeOS = "6"
    androidOSP = "7"
    androidDeviceAdministrator = "8"
    androidWorkProfile = "9"
    androidDedicatedAndFullyManaged = "10"
    unknownFutureValue = "11"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DetectedAppPlatformType"
