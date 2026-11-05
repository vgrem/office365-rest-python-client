from __future__ import annotations

from office365.runtime.client_value import ClientValue


class InboundOutboundPolicyConfiguration(ClientValue):
    inboundAllowed: bool | None = None
    outboundAllowed: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InboundOutboundPolicyConfiguration"
