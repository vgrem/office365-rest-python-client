from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.webauthn_authentication_extensions_client_outputs import (
    WebauthnAuthenticationExtensionsClientOutputs,
)
from office365.directory.authentication.webauthn_authenticator_attestation_response import (
    WebauthnAuthenticatorAttestationResponse,
)
from office365.runtime.client_value import ClientValue


@dataclass
class WebauthnPublicKeyCredential(ClientValue):
    clientExtensionResults: WebauthnAuthenticationExtensionsClientOutputs = field(
        default_factory=WebauthnAuthenticationExtensionsClientOutputs
    )
    id: str | None = None
    response: WebauthnAuthenticatorAttestationResponse = field(default_factory=WebauthnAuthenticatorAttestationResponse)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebauthnPublicKeyCredential"
