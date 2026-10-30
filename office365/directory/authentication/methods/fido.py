from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.authentication.methods.attestationlevel import AttestationLevel
from office365.directory.authentication.methods.method import AuthenticationMethod
from office365.directory.authentication.methods.passkey_type import PasskeyType
from office365.directory.authentication.webauthn_public_key_credential import WebauthnPublicKeyCredential
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class Fido2AuthenticationMethod(AuthenticationMethod):
    """Representation of a FIDO2 security key registered to a user. FIDO2 is a sign-in authentication method."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @odata(name="attestationCertificates")
    @property
    def attestation_certificates(self) -> StringCollection:
        """The attestation certificate(s) attached to this security key."""
        return self.properties.get("attestationCertificates", StringCollection())

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """The timestamp when this key was registered to the user."""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """The display name of the key as given by the user."""
        return self.properties.get("displayName", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """The manufacturer-assigned model of the FIDO2 security key."""
        return self.properties.get("model", None)

    @odata(name="aaGuid")
    @property
    def aa_guid(self) -> Optional[str]:
        """Gets the aaGuid property"""
        return self.properties.get("aaGuid", None)

    @odata(name="attestationLevel")
    @property
    def attestation_level(self) -> AttestationLevel:
        """Gets the attestationLevel property"""
        return self.properties.get("attestationLevel", AttestationLevel.attested)

    @odata(name="passkeyType")
    @property
    def passkey_type(self) -> PasskeyType:
        """Gets the passkeyType property"""
        return self.properties.get("passkeyType", PasskeyType.deviceBound)

    @odata(name="publicKeyCredential")
    @property
    def public_key_credential(self) -> WebauthnPublicKeyCredential:
        """Gets the publicKeyCredential property"""
        return self.properties.get("publicKeyCredential", WebauthnPublicKeyCredential())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Fido2AuthenticationMethod"
