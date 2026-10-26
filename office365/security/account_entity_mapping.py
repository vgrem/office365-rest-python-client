from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AccountEntityMapping(ClientValue):
    aadUserIdColumn: str | None = None
    dnsDomainColumn: str | None = None
    nameColumn: str | None = None
    ntDomainColumn: str | None = None
    sidColumn: str | None = None
    upnColumn: str | None = None
    upnSuffixColumn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AccountEntityMapping"
