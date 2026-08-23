from __future__ import annotations

from office365.runtime.client_value import ClientValue


class StickyRoutingOptions(ClientValue):
    InteractionId: str | None = None
    SessionId: str | None = None
    SessionTicket: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Internal.StickyRoutingOptions"
