from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UserDirectoryInfo(ClientValue):
    """User information from directory service."""

    Name: str | None = None
    NetId: str | None = None
    PrimaryEmail: str | None = None
    PrincipalName: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.UserDirectoryInfo"
