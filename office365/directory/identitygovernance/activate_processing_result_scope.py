from __future__ import annotations
from dataclasses import dataclass
from office365.directory.identitygovernance.activation_task_scope_type import ActivationTaskScopeType
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from office365.entity_collection import EntityCollection
from dataclasses import dataclass, field

@dataclass
class ActivateProcessingResultScope(ClientValue):
    taskScope: ActivationTaskScopeType = ActivationTaskScopeType.allTasks
    processingResults: EntityCollection[UserProcessingResult] | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.identityGovernance.ActivateProcessingResultScope'