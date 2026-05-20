from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.users.id_info import UserIdInfo


@dataclass
class Principal(ClientValue):
    """Principal class is a representation of an identity (user/group)."""

    id: str | None = None
    directoryObjectId: str | None = None
    email: str | None = None
    expiration: str | None = None
    isActive: bool | None = None
    isExternal: bool | None = None
    jobTitle: str | None = None
    loginName: str | None = None
    name: str | None = None
    principalType: int | None = None
    userId: UserIdInfo = field(default_factory=UserIdInfo)
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.Principal"
