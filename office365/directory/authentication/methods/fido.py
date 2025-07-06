from datetime import datetime
from typing import Optional

from office365.directory.authentication.methods.method import AuthenticationMethod
from office365.runtime.types.collections import StringCollection


class Fido2AuthenticationMethod(AuthenticationMethod):
    """Representation of a FIDO2 security key registered to a user. FIDO2 is a sign-in authentication method."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def attestation_certificates(self) -> StringCollection:
        """The attestation certificate(s) attached to this security key."""
        return self.properties.get("attestationCertificates", StringCollection())

    @property
    def created_datetime(self) -> datetime:
        """The timestamp when this key was registered to the user."""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def display_name(self) -> Optional[str]:
        """The display name of the key as given by the user."""
        return self.properties.get("displayName", None)

    @property
    def model(self) -> Optional[str]:
        """The manufacturer-assigned model of the FIDO2 security key."""
        return self.properties.get("model", None)
