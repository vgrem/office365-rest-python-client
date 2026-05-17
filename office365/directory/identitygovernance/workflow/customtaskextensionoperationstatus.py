from enum import Enum


class CustomTaskExtensionOperationStatus(Enum):
    none_ = "-1"
    completed = "0"
    failed = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.CustomTaskExtensionOperationStatus"
