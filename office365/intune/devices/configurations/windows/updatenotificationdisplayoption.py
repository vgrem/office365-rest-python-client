from enum import Enum


class WindowsUpdateNotificationDisplayOption(Enum):
    notConfigured = "0"
    defaultNotifications = "1"
    restartWarningsOnly = "2"
    disableAllNotifications = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsUpdateNotificationDisplayOption"
