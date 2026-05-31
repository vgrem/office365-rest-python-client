from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.directory.identities.userflows.usertype import UserType

@dataclass
class OnUserCreateStartExternalUsersSelfServiceSignUp(ClientValue):
    userTypeToCreate: UserType = UserType.member

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OnUserCreateStartExternalUsersSelfServiceSignUp'