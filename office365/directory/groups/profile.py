from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class GroupProfile(ClientValue):
    mailNickname: str = ""
    displayName: str = ""
    description: str | None = None
    mailEnabled: bool = False
    securityEnabled: bool = True
    owners: list[str] | None = None
    members: list[str] | None = None
    groupTypes: StringCollection = field(default_factory=StringCollection)
