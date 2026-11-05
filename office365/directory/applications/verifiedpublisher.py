from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class VerifiedPublisher(ClientValue):
    addedDateTime: datetime | None = None
    displayName: str | None = None
    verifiedPublisherId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.VerifiedPublisher"
