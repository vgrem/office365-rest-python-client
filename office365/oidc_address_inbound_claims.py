from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class OidcAddressInboundClaims(ClientValue):
    country: str | None = None
    locality: str | None = None
    postal_code: str | None = None
    region: str | None = None
    street_address: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OidcAddressInboundClaims'