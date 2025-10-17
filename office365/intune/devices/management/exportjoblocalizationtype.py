from enum import Enum


class DeviceManagementExportJobLocalizationType(Enum):
    localizedValuesAsAdditionalColumn = "0"
    replaceLocalizableValues = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceManagementExportJobLocalizationType"
