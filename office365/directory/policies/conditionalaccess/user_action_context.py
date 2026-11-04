from __future__ import annotations

from office365.directory.policies.conditionalaccess.useraction import UserAction
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserActionContext(ClientValue):
    userAction: UserAction = UserAction.registerSecurityInformation

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserActionContext"
