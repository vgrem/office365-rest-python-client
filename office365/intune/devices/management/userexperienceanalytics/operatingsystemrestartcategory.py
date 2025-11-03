from enum import Enum


class UserExperienceAnalyticsOperatingSystemRestartCategory(Enum):
    unknown = "0"
    restartWithUpdate = "1"
    restartWithoutUpdate = "2"
    blueScreen = "3"
    shutdownWithUpdate = "4"
    shutdownWithoutUpdate = "5"
    longPowerButtonPress = "6"
    bootError = "7"
    update = "8"
    unknownFutureValue = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserExperienceAnalyticsOperatingSystemRestartCategory"
