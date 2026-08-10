from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class MailboxDetails(ClientValue):
    emailAddress: str | None = None
    externalDirectoryObjectId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailboxDetails"
