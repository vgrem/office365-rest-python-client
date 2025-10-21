from enum import Enum


class DeviceManagementReportStatus(Enum):
    unknown = "0"
    notStarted = "1"
    inProgress = "2"
    completed = "3"
    failed = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementReportStatus"
