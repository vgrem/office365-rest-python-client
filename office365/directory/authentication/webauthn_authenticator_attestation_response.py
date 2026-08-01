from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class WebauthnAuthenticatorAttestationResponse(ClientValue):
    attestationObject: str | None = None
    clientDataJSON: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebauthnAuthenticatorAttestationResponse"
