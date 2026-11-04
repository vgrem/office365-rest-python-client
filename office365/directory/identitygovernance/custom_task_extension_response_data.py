from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.workflow.customtaskextensionoperationstatus import (
    CustomTaskExtensionOperationStatus,
)
from office365.directory.identitygovernance.workflow.subject import WorkflowSubject
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class CustomTaskExtensionResponseData(ClientValue):
    operationStatus: CustomTaskExtensionOperationStatus = CustomTaskExtensionOperationStatus.unknown
    statusReasons: StringCollection = field(default_factory=StringCollection)
    targetSubject: WorkflowSubject = field(default_factory=WorkflowSubject)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.CustomTaskExtensionResponseData"
