from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from office365.runtime.client_value import ClientValue


@dataclass
class PasswordCredential(ClientValue):
    """Represents a password credential associated with an application or a service principal.
    The passwordCredentials property of the application entity is a collection of passwordCredential objects.
    """

    displayName: str | None = None
    secretText: str | None = None
    keyId: str | None = None
    startDateTime: datetime = field(default_factory=lambda: datetime.min)
    endDateTime: datetime = field(default_factory=lambda: datetime.min)
    customKeyIdentifier: bytes | None = None
    hint: str | None = None

    @property
    def is_expired(self) -> bool:
        """True if the credential's end date has passed."""
        if self.endDateTime is None or self.endDateTime == datetime.min:
            return False
        return self.endDateTime < datetime.now(timezone.utc)

    @property
    def days_until_expiry(self) -> int | None:
        """Number of days until expiry, or None if no end date is set."""
        if self.endDateTime is None or self.endDateTime == datetime.min:
            return None
        return (self.endDateTime - datetime.now(timezone.utc)).days

    def __str__(self):
        return str(self.displayName or self.entity_type_name or "")

    @property
    def entity_type_name(self):
        return None
