from enum import Enum


class IosUpdatesInstallStatus(Enum):
    deviceOsHigherThanDesiredOsVersion = "-2016330696"
    sharedDeviceUserLoggedInError = "-2016330699"
    notSupportedOperation = "-2016330701"
    installFailed = "-2016330702"
    installPhoneCallInProgress = "-2016330703"
    installInsufficientPower = "-2016330704"
    installInsufficientSpace = "-2016330705"
    installing = "-2016330706"
    downloadInsufficientNetwork = "-2016330707"
    downloadInsufficientPower = "-2016330708"
    downloadInsufficientSpace = "-2016330709"
    downloadRequiresComputer = "-2016330710"
    downloadFailed = "-2016330711"
    downloading = "-2016330712"
    success = "0"
    available = "1"
    idle = "2"
    unknown = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IosUpdatesInstallStatus"
