from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class VerifiedPublisher(ClientValue):
    addedDateTime: datetime | None = None
    displayName: str | None = None
    verifiedPublisherId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.VerifiedPublisher"
