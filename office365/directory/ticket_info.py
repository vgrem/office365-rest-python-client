from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TicketInfo(ClientValue):
    ticketNumber: str | None = None
    ticketSystem: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TicketInfo"
