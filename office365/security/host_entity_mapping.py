from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class HostEntityMapping(ClientValue):
    deviceIdColumn: str | None = None
    dnsDomainColumn: str | None = None
    nameColumn: str | None = None
    netBiosNameColumn: str | None = None
    ntDomainColumn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostEntityMapping"
