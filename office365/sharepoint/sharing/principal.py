from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.users.id_info import UserIdInfo


@dataclass
class Principal(ClientValue):
    """
    Principal class is a representation of an identity (user/group).

    Fields:
        id: Id of the Principal in SharePoint's UserInfo List.
        email: Email address of the Principal.
        isActive: Boolean value representing if the Principal is Active.
        isExternal: Boolean value representing if the Principal is an external user.
        jobTitle: The Job Title of the Principal.
        loginName: LoginName of the Principal.
        name: Name of the Principal.
    """

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
