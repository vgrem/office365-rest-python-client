from office365.directory.identitygovernance.workflow.customtaskextensionoperationstatus import (
    CustomTaskExtensionOperationStatus,
)
from office365.runtime.client_value import ClientValue


class CustomTaskExtensionCallbackData(ClientValue):
    def __init__(self, operation_status: CustomTaskExtensionOperationStatus = CustomTaskExtensionOperationStatus.none_):
        self.operationStatus = operation_status

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.CustomTaskExtensionCallbackData"
