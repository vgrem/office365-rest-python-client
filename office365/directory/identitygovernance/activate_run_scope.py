from __future__ import annotations

from office365.directory.identitygovernance.activation_task_scope_type import ActivationTaskScopeType
from office365.directory.identitygovernance.activation_user_scope_type import ActivationUserScopeType
from office365.directory.identitygovernance.run import Run
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ActivateRunScope(ClientValue):
    taskScope: ActivationTaskScopeType = ActivationTaskScopeType.allTasks
    userScope: ActivationUserScopeType = ActivationUserScopeType.allUsers
    run: Run | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.ActivateRunScope"
