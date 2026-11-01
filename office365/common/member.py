from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.security.recipient_type import RecipientType


@dataclass
class Member(ClientValue):
    displayName: str | None = None
    key: str | None = None
    memberId: str | None = None
    type: RecipientType = RecipientType.user

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Member"
