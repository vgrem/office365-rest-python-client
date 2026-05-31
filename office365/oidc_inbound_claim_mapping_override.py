from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class OidcInboundClaimMappingOverride(ClientValue):
    address: OidcAddressInboundClaims = field(default_factory=OidcAddressInboundClaims)
    email: str | None = None
    email_verified: str | None = None
    family_name: str | None = None
    given_name: str | None = None
    name: str | None = None
    phone_number: str | None = None
    phone_number_verified: str | None = None
    sub: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OidcInboundClaimMappingOverride'