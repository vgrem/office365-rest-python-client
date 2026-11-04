from __future__ import annotations

from office365.directory.identitygovernance.workflow.customtaskextensionoperationstatus import (
    CustomTaskExtensionOperationStatus,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomTaskExtensionCallbackData(ClientValue):
    operationStatus: CustomTaskExtensionOperationStatus = CustomTaskExtensionOperationStatus.unknown

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.CustomTaskExtensionCallbackData"
