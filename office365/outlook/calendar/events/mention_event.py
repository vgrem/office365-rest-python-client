from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class MentionEvent(ClientValue):
    eventDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    speaker: IdentitySet = field(default_factory=IdentitySet)
    transcriptUtterance: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MentionEvent"
