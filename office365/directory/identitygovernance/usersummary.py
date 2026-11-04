from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserSummary(ClientValue):
    failedTasks: int | None = None
    failedUsers: int | None = None
    successfulUsers: int | None = None
    totalTasks: int | None = None
    totalUsers: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.UserSummary"
