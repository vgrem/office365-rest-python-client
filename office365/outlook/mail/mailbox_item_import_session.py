from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class MailboxItemImportSession(ClientValue):
    expirationDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    importUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailboxItemImportSession"
