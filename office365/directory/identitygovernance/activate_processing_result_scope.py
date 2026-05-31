from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.activation_task_scope_type import ActivationTaskScopeType
from office365.runtime.client_value import ClientValue


@dataclass
class ActivateProcessingResultScope(ClientValue):
    taskScope: ActivationTaskScopeType = ActivationTaskScopeType.allTasks

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.ActivateProcessingResultScope"
