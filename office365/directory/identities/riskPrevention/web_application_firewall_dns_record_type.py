from __future__ import annotations

from enum import Enum


class WebApplicationFirewallDnsRecordType(Enum):
    cname = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallDnsRecordType"
