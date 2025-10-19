from enum import Enum


class AppLockerApplicationControlType(Enum):
    notConfigured = "0"
    enforceComponentsAndStoreApps = "1"
    auditComponentsAndStoreApps = "2"
    enforceComponentsStoreAppsAndSmartlocker = "3"
    auditComponentsStoreAppsAndSmartlocker = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppLockerApplicationControlType"
