from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.webauthn_authentication_extensions_client_inputs import (
    WebauthnAuthenticationExtensionsClientInputs,
)
from office365.directory.authentication.webauthn_authenticator_selection_criteria import (
    WebauthnAuthenticatorSelectionCriteria,
)
from office365.directory.authentication.webauthn_public_key_credential_descriptor import (
    WebauthnPublicKeyCredentialDescriptor,
)
from office365.directory.authentication.webauthn_public_key_credential_parameters import (
    WebauthnPublicKeyCredentialParameters,
)
from office365.directory.authentication.webauthn_public_key_credential_rp_entity import (
    WebauthnPublicKeyCredentialRpEntity,
)
from office365.directory.authentication.webauthn_public_key_credential_user_entity import (
    WebauthnPublicKeyCredentialUserEntity,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class WebauthnPublicKeyCredentialCreationOptions(ClientValue):
    attestation: str | None = None
    authenticatorSelection: WebauthnAuthenticatorSelectionCriteria = field(
        default_factory=WebauthnAuthenticatorSelectionCriteria
    )
    challenge: str | None = None
    excludeCredentials: ClientValueCollection[WebauthnPublicKeyCredentialDescriptor] = field(
        default_factory=lambda: ClientValueCollection(WebauthnPublicKeyCredentialDescriptor)
    )
    extensions: WebauthnAuthenticationExtensionsClientInputs = field(
        default_factory=WebauthnAuthenticationExtensionsClientInputs
    )
    pubKeyCredParams: ClientValueCollection[WebauthnPublicKeyCredentialParameters] = field(
        default_factory=lambda: ClientValueCollection(WebauthnPublicKeyCredentialParameters)
    )
    rp: WebauthnPublicKeyCredentialRpEntity = field(default_factory=WebauthnPublicKeyCredentialRpEntity)
    timeout: int | None = None
    user: WebauthnPublicKeyCredentialUserEntity = field(default_factory=WebauthnPublicKeyCredentialUserEntity)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebauthnPublicKeyCredentialCreationOptions"
