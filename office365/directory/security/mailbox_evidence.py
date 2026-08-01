from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class MailboxEvidence(ClientValue):
    displayName: str | None = None
    primaryAddress: str | None = None
    upn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.MailboxEvidence"
