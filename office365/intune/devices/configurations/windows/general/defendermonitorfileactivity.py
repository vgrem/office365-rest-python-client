from enum import Enum


class DefenderMonitorFileActivity(Enum):
    userDefined = "0"
    disable = "1"
    monitorAllFiles = "2"
    monitorIncomingFilesOnly = "3"
    monitorOutgoingFilesOnly = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DefenderMonitorFileActivity"
