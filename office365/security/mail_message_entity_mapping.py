from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class MailMessageEntityMapping(ClientValue):
    networkMessageIdColumn: str | None = None
    recipientColumn: str | None = None
    senderColumn: str | None = None
    subjectColumn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.MailMessageEntityMapping"
