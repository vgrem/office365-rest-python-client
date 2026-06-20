from __future__ import annotations

from enum import Enum


class WebApplicationFirewallProviderType(Enum):
    akamai = "0"
    cloudflare = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallProviderType"
