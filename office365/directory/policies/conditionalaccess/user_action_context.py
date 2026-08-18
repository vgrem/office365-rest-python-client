from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.conditionalaccess.useraction import UserAction
from office365.runtime.client_value import ClientValue


@dataclass
class UserActionContext(ClientValue):
    userAction: UserAction = UserAction.registerSecurityInformation

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserActionContext"
