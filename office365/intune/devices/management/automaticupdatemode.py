from enum import Enum


class AutomaticUpdateMode(Enum):
    userDefined = "0"
    notifyDownload = "1"
    autoInstallAtMaintenanceTime = "2"
    autoInstallAndRebootAtMaintenanceTime = "3"
    autoInstallAndRebootAtScheduledTime = "4"
    autoInstallAndRebootWithoutEndUserControl = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AutomaticUpdateMode"
