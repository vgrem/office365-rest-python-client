from __future__ import annotations
from dataclasses import dataclass
from office365.directory.identitygovernance.activation_task_scope_type import ActivationTaskScopeType
from office365.directory.identitygovernance.activation_user_scope_type import ActivationUserScopeType
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.directory.identitygovernance.activation_task_scope_type import ActivationTaskScopeType
from office365.directory.identitygovernance.activation_user_scope_type import ActivationUserScopeType
from office365.runtime.paths.resource_path import ResourcePath

@dataclass
class ActivateRunScope(ClientValue):
    taskScope: ActivationTaskScopeType = ActivationTaskScopeType.allTasks
    userScope: ActivationUserScopeType = ActivationUserScopeType.allUsers
    run: Run | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.identityGovernance.ActivateRunScope'