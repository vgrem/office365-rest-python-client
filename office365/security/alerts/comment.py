from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class AlertComment(ClientValue):
    """An analyst-generated comment that is associated with an alert or incident."""

    comment: str | None = None
    createdByDisplayName: str | None = None
    createdDateTime: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AlertComment"
