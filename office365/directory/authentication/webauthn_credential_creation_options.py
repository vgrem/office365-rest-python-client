from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.authentication.webauthn_public_key_credential_creation_options import (
    WebauthnPublicKeyCredentialCreationOptions,
)
from office365.runtime.client_value import ClientValue


@dataclass
class WebauthnCredentialCreationOptions(ClientValue):
    challengeTimeoutDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    publicKey: WebauthnPublicKeyCredentialCreationOptions = field(
        default_factory=WebauthnPublicKeyCredentialCreationOptions
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebauthnCredentialCreationOptions"
