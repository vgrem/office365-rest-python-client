from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.users.password_profile import PasswordProfile
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class UserProfile(ClientValue):
    userPrincipalName: str = ""
    passwordProfile: PasswordProfile = field(default_factory=PasswordProfile)
    mailNickname: str = ""
    displayName: str = ""
    accountEnabled: bool = False
    givenName: str | None = None
    companyName: str | None = None
    businessPhones: StringCollection = field(default_factory=StringCollection)
    officeLocation: str | None = None
    city: str | None = None
    country: str | None = None
