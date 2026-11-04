from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.user_account import UserAccount


@value
class MailboxEvidence(ClientValue):
    displayName: str | None = None
    primaryAddress: str | None = None
    upn: str | None = None
    userAccount: UserAccount = field(default_factory=UserAccount)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.MailboxEvidence"
