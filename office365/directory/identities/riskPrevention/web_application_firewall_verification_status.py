from __future__ import annotations

from enum import Enum


class WebApplicationFirewallVerificationStatus(Enum):
    success = "0"
    warning = "1"
    failure = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallVerificationStatus"
