from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class DomainState(ClientValue):
    lastActionDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    operation: str | None = None
    status: str | None = None
    "Represents the status of asynchronous operations scheduled on a domain."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainState"
