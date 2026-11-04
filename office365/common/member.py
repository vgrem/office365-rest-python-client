from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.recipient_type import RecipientType


@value
class Member(ClientValue):
    displayName: str | None = None
    key: str | None = None
    memberId: str | None = None
    type: RecipientType = RecipientType.user

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Member"
