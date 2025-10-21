from enum import Enum


class DeviceManagementReportFileFormat(Enum):
    csv = "0"
    pdf = "1"
    json = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementReportFileFormat"
