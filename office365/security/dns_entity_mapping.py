from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DnsEntityMapping(ClientValue):
    domainNameColumn: str | None = None
    hostIpAddressColumn: str | None = None
    serverIpColumn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DnsEntityMapping"
