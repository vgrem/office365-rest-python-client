from enum import Enum


class IosNotificationAlertType(Enum):
    deviceDefault = "0"
    banner = "1"
    modal = "2"
    none = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IosNotificationAlertType"
