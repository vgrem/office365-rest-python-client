from __future__ import annotations

from office365.directory.credential import Credential
from office365.runtime.types.value import value


@value
class PasswordCredential(Credential):
    """Represents a password credential (client secret) associated with an
    application or a service principal. The passwordCredentials property of the
    application entity is a collection of passwordCredential objects.
    """

    secretText: str | None = None
    customKeyIdentifier: bytes | None = None
    hint: str | None = None

    @property
    def kind(self) -> str:
        """Human-friendly credential kind label."""
        return "Password"

    def __str__(self):
        return self.displayName or self.hint or "(unnamed)"

    @property
    def entity_type_name(self):
        return None
