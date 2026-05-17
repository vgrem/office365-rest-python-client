from enum import Enum


class AutoRestartNotificationDismissalMethod(Enum):
    notConfigured = "0"
    automatic = "1"
    user = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AutoRestartNotificationDismissalMethod"
