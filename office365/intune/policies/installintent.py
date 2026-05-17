from enum import Enum


class InstallIntent(Enum):
    available = "0"
    required = "1"
    uninstall = "2"
    availableWithoutEnrollment = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.InstallIntent"
