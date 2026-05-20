from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UserDirectoryInfo(ClientValue):
    """
    User information from directory service.

    Fields:
        Name: Principal name of the directory user. E.g. user@domain.com.
        NetId: User NetId property in directory.
        PrimaryEmail: User primary email of the directory user. E.g. user@domain.com.
        PrincipalName: Principal name of the directory user. E.g. user@domain.com.
    """

    Name: str | None = None
    NetId: str | None = None
    PrimaryEmail: str | None = None
    PrincipalName: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.UserDirectoryInfo"
