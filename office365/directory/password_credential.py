from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class PasswordCredential(ClientValue):
    """Represents a password credential associated with an application or a service principal.
    The passwordCredentials property of the application entity is a collection of passwordCredential objects.
    """

    displayName: str | None = None
    secretText: str | None = None
    keyId: str | None = None
    startDateTime: datetime | None = None
    endDateTime: datetime | None = None
    customKeyIdentifier: bytes | None = None
    hint: str | None = None

    def __str__(self):
        return str(self.displayName or self.entity_type_name or "")

    @property
    def entity_type_name(self):
        return None
